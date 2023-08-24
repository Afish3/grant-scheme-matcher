from flask import Flask, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from dotenv import load_dotenv
import pickle
import os

from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback

from pdfs import Pdf 

app = Flask(__name__)

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

app.debug = True


@app.route('/')
def index():
    load_dotenv()
    return render_template('base.html')
    
@app.route('/form')
def handle_form():
    # get the pdf text
    if os.path.exists('all_grants.pkl'):
        with open("all_grants.pkl", "rb") as f:
                knowledge_base = pickle.load(f)
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


# Each grant will be associated with a number. 
# Forestry Grant Scheme: 1
# Forestry Co-op scheme: 2
# Future Woodlands Fund: 3
# Crofting Agricultural Grant Scheme: 4
# Croft Woodland Project, MoreWoods: 5
# South of Scotland Tree Planting Grant Scheme: 6
# Only return a list of numbers for grants that the applicant could be eligible for.