from flask import Flask, redirect, render_template, session, json, request, jsonify, flash, url_for
from flask_debugtoolbar import DebugToolbarExtension
from dotenv import load_dotenv
import pickle
import os

from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback

from pdfs import Pdf 
from forms import GrantForm, questions
from model import connect_db, db, User, Grants

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///grant-matcher"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.debug = True
app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def index():
    load_dotenv()
    return render_template('base.html')

@app.route('/start_form')
def start_form():
    """
    Initialized a WTForm instance for validatioin and handles subsequent questions through AJAX requests through JavaScript.

    This route should be hit once for the showing of the form.
    """
    form = GrantForm()

    return render_template('test.html', form=form, current_question=0)

@app.route('/session', methods=['POST'])
def setting_session():
    """Post request route that redirects to the start of the survey after setting a session cookie to track user responses in a list.    
    """
    session['responses'] = []
    print(session['responses'])
    return redirect('/form/question/0')

@app.route('/form/question/<int:num>', methods=['POST', 'GET'])
def show_question(num):
    """Form path question by question.

    The form questions correspond to the number of items in the list of responses

    >>> num == len(session['responses'])
    True
    """
    form = GrantForm()
    responses = session.get('responses')

    # # if request.method == 'POST':
    # #     if responses is None:
    # #         responses = {}
    # #     if request.data is not None:
    # #         data = json.loads(request.data)
    # #         responses[f'q{num}'] = data.get(f'q{num}')
    # #         session.set('responses', responses)
    # #     raise

    #     if len(responses.keys()) != num:
    #         flash('Please complete the form in order as the questions come up...', 'error')
    #         flash('Thank you!', 'error')
    #         return redirect(f'/form/question/{len(responses)}')
    #     elif num >= len(questions) and (len(responses.keys()) == len(questions)):
    #         flash('Thank you for taking the time to fill out the form!', 'success')
    #         flash('WOOHOO! Here are some grants you may be elgibile for...', 'success')
    #         return redirect(url_for(handle_form)) 
    
    next_question = GrantForm.get_next_question(form)
    if next_question is not None:
        form_html = next_question.json['form']
        question = next_question.json['question']
        return render_template('questions.html', form=form, question=question, form_html=form_html, num=num)
    return render_template('errors.html')

@app.route('/post/response/<int:num>', methods=['POST'])
def post_response(num):
    form = GrantForm()
    responses = session.get('responses')

    if request.method == 'POST':
        if responses is None:
            responses = {}
        data = form.q1.data
        raise
        session.set('responses', responses)
    return redirect(f'/form/question/{num+1}')

@app.route('/form/question/', methods=['POST', 'GET'])
def get_form_question():
    """
    This route serves as an endpoint for AJAX requests made through Javascript that serve questions in the form.
    """
    user = User()
    session['user_id'] = user.id
    form = GrantForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if session.get('user_id') is not None:
                answer = json.loads(request.data)
                print(answer)
                answer.pop('csrf_token')
                user.answers = answer

            return jsonify({"success": True})
        
        print("not validated")
        return jsonify({"error": True})
    
    return GrantForm.get_next_question(form)

@app.route('/form')
def handle_form():
    # get the pdf text
    if os.path.exists('all_grants.pkl'):
        with open("all_grants.pkl", "rb") as f:
                knowledge_base = pickle.load(f)
        knowledge_base = Pdf.get_embedded_text_chunks()
    else:
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

    # data = form.data
    msg = f"""
        A potential grant applicant meets these criteria.
        Land Owner,
        Size of Site: Over 10 hectares,
        Current Land Use: Public Land, not a croft,
        Age of the Project: Old,
        Are there any legal requirements for planting: Yes,
        Individual or group owned/managed land: Group,
        Age of land owner(s)/manager(s): All less than 41
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
        """
    matching_documents = knowledge_base.similarity_search(msg)

    llm = OpenAI()
    chain = load_qa_chain(llm, chain_type='stuff')
    with get_openai_callback() as callback:
        res = chain.run(input_documents=matching_documents, question=msg)
        print(callback)

    # import json
    # import requests
    # HUGGINGFACEHUB_API_TOKEN = os.environ.get("HUGGINGFACEHUB_API_TOKEN")
    # headers = {"Authorization": f"Bearer {HUGGINGFACEHUB_API_TOKEN}"}
    # API_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
    # def query(payload):
    #     data = json.dumps(payload)
    #     response = requests.request("POST", API_URL, headers=headers, data=data)
    #     return json.loads(response.content.decode("utf-8"))
    # data = query(
    #     {
    #         "inputs": {
    #             "question": prompt,
    #             "context": requirements,
    #         }
    #     }
    # )

    grants_list = [int(x) for x in res.split(',')]

    return render_template('response.html', res=res)
