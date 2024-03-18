from dotenv import load_dotenv
import os
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import TextSplitter, RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime
import json
import PyPDF2
import chromadb