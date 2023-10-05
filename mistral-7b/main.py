from ctransformers import AutoModelForCausalLM, AutoTokenizer
from PyPDF2 import PdfReader
import os
from docx import Document
import win32com.client
import csv


ABS_DATA_PATH='F:\python\chat_with_docs\data'
ABS_DATA_PATH= ABS_DATA_PATH.replace('\\', '/')+'/'


class Documents:
    def __init__(self,path='',type=''):
        self._path=path
        self._type=''
        self._text=''
    def get_path(self):
        return self._path
    def get_type(self):
        return self._type
    def get_text(self):
        return self._text
    def set_path(self,path):
        self._path=path
    def set_type(self,type):
        self._type=type
    def set_text(self,text):
        self._text=text
    
        