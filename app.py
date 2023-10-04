from flask import Flask, redirect, render_template, session, json, request, jsonify, flash, url_for
from flask_debugtoolbar import DebugToolbarExtension
from collections import OrderedDict
from dotenv import load_dotenv
import pickle
import os

from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback

from pdfs import Pdf 
from forms import GrantForm, questions, grant_data
from model import db, connect_db, User, Grants, track_new_form_submission

app = Flask(__name__)

secret_key = os.getenv("SECRET_KEY")
database_url = os.getenv("DATABASE_URL")

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SECRET_KEY"] = secret_key

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# app.debug = True
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
    """Home page check the session to see if the form has been filled out before. If it has the results template is returned showing applicable grants. Approximate calculations of money that could be recieved are calculated with the Grant class method calculate_amount and passed to the template.
    
    else, the home page is shown to start filling out the form.
    """
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

@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""

    return render_template('404.html'), 404

@app.route('/form/question/<int:num>')
def show_question(num):
    """Form path question by question.

    The form questions correspond to the number of items in the list of responses plus 1.

    >>> num == len(session['responses']) + 1
    True

    questions are generated in order by calling the get_next_question class method on the GrantForm in forms.py.
    """
    form = GrantForm()
    responses = session.get('responses', OrderedDict())

    if len(responses.keys()) != num - 1:
        return redirect(f'/form/question/{len(responses)+1}')
    elif num >= len(questions) and (len(responses.keys()) == len(questions)):
        flash('Thank you for taking the time to fill out the form!', 'success')

        # Sumbit all answers to ai functionality.
        return redirect(url_for('handle_form'))
    
    next_question = GrantForm.get_next_question(form, num)
    if next_question is not None:
        form_html = next_question.json['form']
        question = next_question.json['question']

        # Calculate progress for progress bar on the form
        progress = str(round(get_progress(len(questions), num)))
        return render_template('questions.html', form=form, question=question, form_html=form_html, num=num, progress_so_far=progress)
    return render_template('errors.html')

@app.route('/post/response/<int:num>', methods=['POST'])
def post_response(num):
    """Form answer post path. Responses to questions are added to a dictionary and saved in the session.
    """
    form = GrantForm()
    responses = session.get('responses')

    if request.method == 'POST':
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
    del responses[questions[num-1]]
    session['responses'] = responses
    
    return redirect(url_for('show_question', num=num))

@app.route('/form')
def handle_form():
    """
    knowledge_base is created by creating the all_grants.pkl file that holds the vectored grant information from grant scheme pdfs.

    User responses are sent as a string along with knowledge base to handle_ai_similarity_search function for AI analysis. 
    
    The LLM's response is converted to a list of integers representing the grants that are applicable to the user to be stored in session and displayed at the root path '/' 
    
    """

    responses_dict = session.get('responses')
    responses_text = ''
    for key, value in responses_dict.items():
        responses_text += f'{key}: {value}, '
    
    knowledge_base = get_knowledge_base()
    res = handle_ai_similarity_search(responses_text, knowledge_base)

    try:
        grants_list = [int(x) for x in res.split(',')]
    except ValueError:
        return redirect(url_for('handle_form'))

    session['eligible_grants'] = grants_list
    track_new_form_submission(grants_list, responses_dict)

    return redirect(url_for('index'))

@app.route('/restart')
def restart():
    """
    Reset session and start a new form to find grants.
    """
    session['responses'] = {}
    session['eligible_grants'] = None
    return redirect(url_for('show_question', num=1))

def get_knowledge_base():
    """
    Creates a knowledge base for use with the LLM that consists of vectorized text extracted from grant scheme pdf documents.

    knowledge_base will be saved for future use as all_grants.pkl until new grants are added or API keys for vector conversion are changed.
    """
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
