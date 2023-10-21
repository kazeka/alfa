import asyncio
import chromadb
import logging
import sys

from chromadb.config import Settings
from dotenv import load_dotenv, find_dotenv
from os import getenv

from aiogram import Bot, types, Dispatcher

from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import GPT4All, LlamaCpp
from langchain.vectorstores import Chroma
from langchain import PromptTemplate

_ = load_dotenv(find_dotenv())


EMBEDDINGS_MODEL_NAME = getenv('EMBEDDINGS_MODEL_NAME')
PERSIST_DIRECTORY = getenv('PERSIST_DIRECTORY')
CHROMA_SETTINGS = Settings(
        persist_directory=PERSIST_DIRECTORY,
        anonymized_telemetry=False
)

TOKEN = getenv('ATOKEN')
MODEL_TYPE = getenv('MODEL_TYPE')
MODEL_PATH = getenv('MODEL_PATH')
MODEL_N_CTX = getenv('MODEL_N_CTX')
MODEL_N_BATCH = int(getenv('MODEL_N_BATCH', 8))
TARGET_SOURCE_CHUNKS = int(getenv('TARGET_SOURCE_CHUNKS', 4))

TEMPLATE = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}
Answer in Russian:"""


embeddings = HuggingFaceEmbeddings(model_name=EMBEDDINGS_MODEL_NAME)
chroma_client = chromadb.PersistentClient(settings=CHROMA_SETTINGS, path=PERSIST_DIRECTORY)
db = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embeddings, client_settings=CHROMA_SETTINGS, client=chroma_client)
retriever = db.as_retriever(search_kwargs={'k': TARGET_SOURCE_CHUNKS})
callbacks=[StreamingStdOutCallbackHandler()]


match MODEL_TYPE:
    case 'LlamaCpp':
        n_gpu_layers = 40  # Change this value based on your model and your GPU VRAM pool.
        n_batch = 512  # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.
        llm = LlamaCpp(model_path=MODEL_PATH, n_gpu_layers=n_gpu_layers, max_tokens=MODEL_N_CTX, n_ctx=MODEL_N_CTX, n_batch=MODEL_N_BATCH, callbacks=callbacks, verbose=True)
    case 'GPT4All':
        llm = GPT4All(model=MODEL_PATH, max_tokens=MODEL_N_CTX, backend='gptj', n_batch=MODEL_N_BATCH, callbacks=callbacks, verbose=False)

qa = RetrievalQA.from_chain_type(llm=llm, chain_type='stuff', retriever=retriever, return_source_documents=True, chain_type_kwargs={
        'prompt': PromptTemplate(
            template=TEMPLATE,
            input_variables=['context', 'question'],
        ),
    },)


bot = Bot(TOKEN)
dp = Dispatcher(bot=bot)


# @dp.message(Command('start', 'help'))
@dp.message_handler(commands=['start', 'help'])
async def process_command(message: types.Message):
    await message.reply('Привет! Я тестовый чатбот на основе общедоступной информации с сайта. С вопросами обращайтесь к @alex_kazeka. Если я работаю, зачит я обновляюсь)')


# @dp.message()
@dp.message_handler()
async def answer_message(message: types.Message):
    ans = qa({'query': message.text})
    logging.info(ans['source_documents'])
    await message.answer(ans['result'])


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    # bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())