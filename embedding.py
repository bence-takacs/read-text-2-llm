from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import  CharacterTextSplitter # TokenTextSplitter #
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.evaluation.qa import QAEvalChain
import json

# See: https://github.com/hwchase17/langchain/blob/b95002289409077965d99636b15a45300d9c0b9d/docs/use_cases/evaluation/data_augmented_question_answering.ipynb

class Embedding:
  def __init__(self, text_file):
    print('--- Loading text ---')
    loader = TextLoader(text_file)
    documents = loader.load()
    print('--- Splitting text into chunks ---')
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0) # TokenTextSplitter(chunk_size=1000, chunk_overlap=0) #
    texts = text_splitter.split_documents(documents)

    print('--- Init OpenAI embedding API ---')
    embeddings = OpenAIEmbeddings()
    docsearch = Chroma.from_documents(texts, embeddings)
    self.qa = RetrievalQA.from_llm(llm=OpenAI(), retriever=docsearch.as_retriever()) #model='text-davinci-003'

  def query(self, question):
    return self.qa.run(question)

# with open('queries.json', 'r') as f:
#   examples = json.load(f)

# predictions = self.qa.apply(examples)
# llm = OpenAI(temperature=0)

# eval_chain = QAEvalChain.from_llm(llm)
# graded_outputs = eval_chain.evaluate(examples, predictions)
# for i, eg in enumerate(examples):
#     print(f"Example {i}:")
#     print("Question: " + predictions[i]['query'])
#     print("Real Answer: " + predictions[i]['answer'])
#     print("Predicted Answer: " + predictions[i]['result'])
#     print("Predicted Grade: " + graded_outputs[i]['text'])
#     print()
