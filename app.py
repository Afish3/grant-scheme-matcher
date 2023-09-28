from flask import Flask, redirect, render_template, session, json, request, jsonify, flash, url_for
from flask_debugtoolbar import DebugToolbarExtension
from waitress import serve
from collections import OrderedDict
from dotenv import load_dotenv
import pickle
import os

from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback

from pdfs import Pdf 
from forms import GrantForm, questions, grant_data
from model import connect_db, db, User, Grants

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///grant-matcher"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# app.debug = True
# app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# debug = DebugToolbarExtension(app)

connect_db(app)

grant_titles = ["Forestry Grant Scheme", "Forestry Co-op scheme", "Future Woodlands Fund",
                "Crofting Agricultural Grant Scheme", "Croft Woodland Project, MoreWoods",
                "South of Scotland Tree Planting Grant Scheme"]

def get_progress(total, current):
    return (current / total) * 100

def is_string(val):
    return isinstance(val, str)

app.jinja_env.filters['is_string'] = is_string

@app.route('/')
def index():
    load_dotenv()
    if session.get('eligible_grants') is not None:
        grants = session.get('eligible_grants')
        responses_dict = session.get('responses')
        responses = [(key, value) for key, value in responses_dict.items()]
        size = responses[len(responses)-1][1]
        age = responses[len(responses)-4][1]
        amount_of_applicants = responses[len(responses)-3][1]
        for num in grants:
            grant_data[f'g{num}']['amount'] = Grants.calculate_amount(num, size, age, amount_of_applicants)
        return render_template('response.html', grants_list=grants, responses=responses, grant_titles=grant_titles, grant_data=grant_data)
    return render_template('home.html')

@app.route('/form/question/<int:num>')
def show_question(num):
    """Form path question by question.

    The form questions correspond to the number of items in the list of responses

    >>> num == len(session['responses'])
    True
    """
    form = GrantForm()
    responses = session.get('responses', OrderedDict())

    if len(responses.keys()) != num - 1:
        return redirect(f'/form/question/{len(responses)+1}')
    elif num >= len(questions) and (len(responses.keys()) == len(questions)):
        flash('Thank you for taking the time to fill out the form!', 'success')
        flash('WOOHOO! Here are some grants you may be eligibile for...', 'success')
        return redirect(url_for('handle_form'))
    
    next_question = GrantForm.get_next_question(form, num)
    if next_question is not None:
        form_html = next_question.json['form']
        question = next_question.json['question']
        progress = str(round(get_progress(len(questions), num)))
        return render_template('questions.html', form=form, question=question, form_html=form_html, num=num, progress_so_far=progress)
    return render_template('errors.html')

@app.route('/post/response/<int:num>', methods=['POST'])
def post_response(num):
    form = GrantForm()
    responses = session.get('responses')

    if request.method == 'POST':
        print(form.csrf_token)
        if form.validate_on_submit():
            print('Successfully VALIDATED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        else:
            print('Failed to validate!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        if responses is None:
            responses = {}
        data = form.data
        answer = data.get(f'q{num}')
        responses[questions[num-1]] = answer
        session['responses'] =  responses
        print(session['responses'])
    return redirect(f'/form/question/{num+1}')

@app.route('/back')
def go_to_previous_question():
    """Reverses the most recent answer and redirects to the previous question"""
    responses = session.get('responses', {})
    num = len(responses)
    print(responses)
    print(questions[num-1])
    del responses[questions[num-1]]
    session['responses'] = responses
    print(session.get('responses', {}))
    return redirect(url_for('show_question', num=num))

@app.route('/form')
def handle_form():

    responses_dict = session.get('responses')
    responses_text = ''
    for key, value in responses_dict.items():
        responses_text += f'{key}: {value}, '
    
    knowledge_base = get_knowledge_base()
    res = handle_ai_similarity_search(responses_text, knowledge_base)

    grants_list = [int(x) for x in res.split(',')]
    session['eligible_grants'] = grants_list

    return redirect(url_for('index'))

@app.route('/restart')
def restart():
    """
    Reset session and start a new form to find grants.
    """
    session['responses'] = {}
    session['grants'] = None
    return redirect(url_for('show_question', num=1))

def get_knowledge_base():
    if os.path.exists('all_grants.pkl'):
        with open("all_grants.pkl", "rb") as f:
                knowledge_base = pickle.load(f)
    else:
        # get the pdf text
        all_grants_text = ''
        for filename in os.listdir('static/files'):
            path = f'static/files/{filename}'
            if filename != '.DS_Store':
                with open(path, 'r') as f:
                    pdf = Pdf(path)
                    all_grants_text += pdf.read_pdf()

        # get the text in chunks for vector storing
        chunks = Pdf.chunk_pdf_text(all_grants_text)
        
        # create vector store
        knowledge_base = Pdf.get_embedded_text_chunks(chunks)

    return knowledge_base

def handle_ai_similarity_search(responses, knowledge_base):
    """
    This function takes user responses and plugs them into the formulated prompt.

    The function runs a similarity search using the llm with the knowledge base and the prompt and returns the AI response as a list of available grants by number in the form of a string.
    """
    msg = f"""
        A potential grant applicant meets these criteria.
        {responses}
        Based on this information please match them with all grants that they could be eligible for. 
        Each grant will be associated with a number. 
        Forestry Grant Scheme: 1
        Forestry Co-op scheme: 2
        Future Woodlands Fund: 3
        Crofting Agricultural Grant Scheme: 4
        Croft Woodland Project, MoreWoods: 5
        South of Scotland Tree Planting Grant Scheme: 6
        Only return a list of numbers for grants that the applicant could be eligible for.
        An example input and expected output will be wrapped in XML tags.
        Example 1:
        <input>
        A potential grant applicant meets these criteria.
        Land Owner,
        Size of Site: Between 3 and 5 hectares,
        Current Land Use: Croft,
        Age of the Project: New,
        Are there any legal requirements for planting: No,
        Individual or group owned/managed land: Individual,
        Age of land owner/manager: 53
        </input>
        1,3,4 
        Example 2:
        <input>
        A potential grant applicant meets these criteria.
        Land Owner,
        Size of Site: Less than 0.25 hectares,
        Current Land Use: Croft,
        Age of the Project: New,
        Are there any legal requirements for planting: No,
        Individual or group owned/managed land: Individual,
        Age of land owner/manager: 53,
        Is the land in the South of Scotland: Yes
        </input>
        1,3,4,5,6
        """
    matching_documents = knowledge_base.similarity_search(msg)

    llm = OpenAI()
    chain = load_qa_chain(llm, chain_type='stuff')
    with get_openai_callback() as callback:
        res = chain.run(input_documents=matching_documents, question=msg)
        print(callback)

    return res

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=80)
