from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import  CharacterTextSplitter # TokenTextSplitter #
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.chat_models import ChatOpenAI
import json
import logging

# See: https://github.com/hwchase17/langchain/blob/b95002289409077965d99636b15a45300d9c0b9d/docs/use_cases/evaluation/data_augmented_question_answering.ipynb

CHROMA_DB_DIRECTORY = './.chroma'
class Embedding:
  def __init__(self, text_file):
    logging.info('--- Loading text ---')
    loader = TextLoader(text_file)
    documents = loader.load()
    logging.info('--- Splitting text into chunks ---')
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0) # TokenTextSplitter(chunk_size=1000, chunk_overlap=0) #
    texts = text_splitter.split_documents(documents)

    logging.info('--- Init OpenAI embedding API ---')
    embeddings = OpenAIEmbeddings()
    docsearch = Chroma.from_documents(
      texts, 
      embeddings, 
      persist_directory=CHROMA_DB_DIRECTORY
      #     collection_name="ask_django_docs",
    )

    docsearch.persist()
    self.qa = RetrievalQA.from_chain_type(
      llm=ChatOpenAI(temperature=0), 
      chain_type="stuff",
      retriever=docsearch.as_retriever(),
      chain_type_kwargs={"verbose": True}
      #model='text-davinci-003'
    ) 

  def query(self, question):
    return self.qa.run(question)

# with open('queries.json', 'r') as f:
#   examples = json.load(f)

# predictions = self.qa.apply(examples)
# llm = OpenAI(temperature=0)

# eval_chain = QAEvalChain.from_llm(llm)
# graded_outputs = eval_chain.evaluate(examples, predictions)
# for i, eg in enumerate(examples):
#     logging.info(f"Example {i}:")
#     logging.info("Question: " + predictions[i]['query'])
#     logging.info("Real Answer: " + predictions[i]['answer'])
#     logging.info("Predicted Answer: " + predictions[i]['result'])
#     logging.info("Predicted Grade: " + graded_outputs[i]['text'])
