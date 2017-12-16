import json
import logging
import nbformat
import cgi
from nbconvert.preprocessors import ExecutePreprocessor
from io import StringIO, BytesIO
import multipart as mp
from multipart import tob
import base64
import os

os.environ['PYTHONPATH'] = os.getcwd()

logger = logging.getLogger(__name__)

def execute_notebook(source) -> str:
    nb = nbformat.read(source, as_version=4)
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(nb, {'metadata': {'path': '/tmp/'}})

    ex = StringIO()
    nbformat.write(nb, ex)

    return ex.getvalue()

def nbformathandler(event, context):

    headers = event['headers'];
    content_type = headers['content-type']
    boundary = content_type.split('=')[1]
    httpbody = mp.MultipartParser(BytesIO(str.encode(event['body'])), boundary)
    data = httpbody.get('data').file.read()

    in_memory_source = BytesIO(data)
    res = execute_notebook(in_memory_source)

    response = {
        "statusCode": 200,
        "body": res
    }

    return response
