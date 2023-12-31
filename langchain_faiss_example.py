from typing import List
import os

from langchain.callbacks.manager import CallbackManagerForRetrieverRun
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.vectorstores.base import VectorStoreRetriever
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from langchain.document_loaders import TextLoader
from langchain_google_genai import ChatGoogleGenerativeAI
import numpy as np

import streamlit as st
from trulens_eval import feedback
from trulens_eval import Feedback
from trulens_eval import Select
from trulens_eval import Tru

from api_utils import get_entries
from src.Utils.utils import save_to_json

if os.getenv('DEV_ENV'):
    user_api_key = os.getenv('DEV_API_KEY')
    user_email = os.getenv('DEV_EMAIL')
    st.session_state['user_email'] = user_email
    st.session_state['user_api_key'] = user_api_key
else:
    user_email = st.session_state['user_email']
    user_api_key = st.session_state['user_api_key']


# Create a local FAISS Vector DB based on README.md .
# loader = UnstructuredMarkdownLoader("README.md")
    
raw_documents = TextLoader('temp_file.json').load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
documents = text_splitter.split_documents(raw_documents)
# documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(docs, embeddings)

data = get_entries(
    user_email,
    user_api_key,
    )

# storage_context = doc_result = embeddings.embed_documents([data.__str_()])

file_name = "temp_file.json"

save_to_json(data,file_name)

docs = documents = SimpleDirectoryReader(input_files=[file_name]).load_data()


# Save it.
db.save_local("faiss_index")
retriever = db.as_retriever()


class VectorStoreRetrieverWithScore(VectorStoreRetriever):

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        if self.search_type == "similarity":
            docs_and_scores = self.vectorstore.similarity_search_with_relevance_scores(
                query, **self.search_kwargs
            )

            print("From relevant doc in vec store")
            docs = []
            for doc, score in docs_and_scores:
                if score > 0.6:
                    doc.metadata["score"] = score
                    docs.append(doc)
        elif self.search_type == "mmr":
            docs = self.vectorstore.max_marginal_relevance_search(
                query, **self.search_kwargs
            )
        else:
            raise ValueError(f"search_type of {self.search_type} not allowed.")
        return docs

# Create the example app.
class FAISSWithScore(FAISS):

    def as_retriever(self) -> VectorStoreRetrieverWithScore:
        return VectorStoreRetrieverWithScore(
            vectorstore=self,
            search_type="similarity",
            search_kwargs={"k": 4},
        )


class FAISSStore:

    @staticmethod
    def load_vector_store():
        embeddings = OpenAIEmbeddings()
        faiss_store = FAISSWithScore.load_local("faiss_index", embeddings)
        print("Faiss vector DB loaded")
        return faiss_store

# Create a feedback function.
openai = feedback.OpenAI()

f_qs_relevance = Feedback(openai.qs_relevance, name = "Context Relevance").on_input().on(
    Select.Record.app.combine_docs_chain._call.args.inputs.input_documents[:].page_content
).aggregate(np.min)

# Bring it all together.
def load_conversational_chain(vector_store):
    # llm = ChatOpenAI(
    #     temperature=0,
    #     model_name="gpt-4",
    # )
    llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    convert_system_message_to_human=True,
    )
    # retriever = vector_store.as_retriever()
    retriever = db.as_retriever()
    chain = ConversationalRetrievalChain.from_llm(
        llm, retriever, return_source_documents=True
    )
    
    tru = Tru()

    truchain = tru.Chain(
        chain,
        feedbacks=[f_qs_relevance],
        with_hugs=False
    )

    return chain, truchain


# Run example:
vector_store = FAISSStore.load_vector_store()
chain, tru_chain_recorder = load_conversational_chain(vector_store)

# with tru_chain_recorder as recording:
#     ret = chain({"question": "What is trulens?", "chat_history":""})

eval_questions = []
with open('data/eval_questions.txt', 'r') as file:
    for line in file:
        # Remove newline character and convert to integer
        item = line.strip()
        eval_questions.append(item)

# Run evaluation engine on each eval question
for question in eval_questions:
    with tru_chain_recorder as recording:
        ret = chain({"question": question, "chat_history":""})

    # with tru_recorder as recording:
    #     # query_engine.query(question)
    #     query_engine({"question":question,"chat_history":""})


Tru().run_dashboard()