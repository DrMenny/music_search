# using Sanic
import json
import traceback
import sanic
import re
from sanic import Sanic, Blueprint
from sanic.exceptions import NotFound
from sanic_openapi import swagger_blueprint
from loko_extensions.business.decorators import extract_value_args
from utils.logger_utils import stream_logger
from ShazamAPI import Shazam
from wikipedia import wikipedia
from sanic_openapi.openapi2 import doc

logger = stream_logger(__name__)

def get_app(name):
    app = Sanic(name)
    swagger_blueprint.url_prefix = "/api"
    app.blueprint(swagger_blueprint)
    return app

name = "first_project"
app = get_app(name)
bp = Blueprint("default", url_prefix=f"/")
app.config["API_TITLE"] = name

@bp.post('/wikipedia_info')
@doc.consumes(doc.JsonBody({"value": {"author": str, "title": str}, "args": {}}), location="body")
@extract_value_args()
async def f(value, args):
    def getsummary(author, title):
        title = re.sub('\(.+\)', '', title).strip()
        logger.debug(f'TITLE: {title}')
        s = author + ' ' + title
        logger.debug(f's: {s}')
        pages = wikipedia.search(s)
        logger.debug(f'RESP: {pages}')
        found = False
        summary = None
        while (pages and not found):
            try:
                summary = wikipedia.summary(pages.pop(0))
                logger.debug(f'SUMMARY: {summary}')
                if (author.lower() in summary.lower()):
                    found = True
                    logger.debug(f'SUM: {summary}')
            except Exception as e:
                logger.debug(f'ERROR: {e}')
        return summary if found else 'Not found'

    logger.debug(f'ARGS: {args}')
    logger.debug(f'JSON: {value}')
    title = value.get('title')
    author = value.get('author')
    logger.debug(f'author: {author} title: {title}')
    return sanic.json(getsummary(author, title))

@bp.post('/upload_file')
@extract_value_args(file=True)
async def f2(file, args):
    logger.debug(f'ARGS: {args}')
    logger.debug(f'JSON: {file[0].name}')
    shazam = Shazam(file[0].body)
    recognize_generator = shazam.recognizeSong()
    res = next(recognize_generator)  # current offset & shazam response to recognize requests
    KeysMapping = dict(subtitle='author', title='title')
    logger.debug(f'RESP: {res}')
    res = {v: res[1]['track'][k] for k, v in KeysMapping.items()}
    return sanic.json(res)

@app.exception(Exception)
async def manage_exception(request, exception):
    e = dict(error=str(exception))
    if isinstance(exception, NotFound):
        return sanic.json(e, status=404)
    logger.error('TracebackERROR: \n' + traceback.format_exc() + '\n\n')
    status_code = exception.status_code or 500
    return sanic.json(e, status=status_code)

app.blueprint(bp)

app.run("0.0.0.0", port=8080, auto_reload=True)