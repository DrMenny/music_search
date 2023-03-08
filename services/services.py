# using Sanic
# import json
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
from urllib.parse import unquote
from bs4 import BeautifulSoup

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
        #logger.debug(f'TITLE: {title}')
        s = author + ' ' + title
        #logger.debug(f's: {s}')
        pages = wikipedia.search(s)
        logger.debug(f'RESP: {pages}')
        found = False
        summary = None
        while (pages and not found):
            try:
                summary = wikipedia.page(pages.pop(0))
                cont = summary.html()
                logger.debug(f'TITLE: {summary.title}')
                #logger.debug(f'PAGES: {cont}')
                music = 'studio album'
                single = 'single'
                if music.lower() in cont.lower() or single.lower() in cont.lower():
                    logger.debug('Studio Album or Single has found')

                    if author.lower() in cont.lower() and title.lower() in cont.lower():
                        author_1 = author.replace(" ", "_")
                        title_1 = title.replace(" ", "_")
                        logger.debug(f'AUTHOR: {author_1}')
                        logger.debug(f'SONG: {title_1}')
                        url_1 = unquote(summary.url)
                        logger.debug(f'URL: {url_1}')
                        if author_1.lower() in url_1.lower() or title_1.lower() in url_1.lower():
                            found = True
                            logger.debug('ok')
                        else:
                            logger.debug('none')
                    else:
                        logger.debug('none')
                else:
                    logger.debug('No Studio Album or Single found')
            except Exception as e:
                logger.debug(f'ERROR: {e}')
        return summary.content if found else 'Not found'

    #logger.debug(f'ARGS: {args}')
    logger.debug(f'VALUES: {value}')
    title = value.get('title')
    author = value.get('author')
    title = re.sub('\(.+\)', '', title).strip()
    logger.debug(f'author: {author} title: {title}')
    return sanic.json(getsummary(author, title))

@bp.post('/upload_file')
@extract_value_args(file=True)
async def f2(file, args):
    #logger.debug(f'JSON: {file[0]}')
    logger.debug(f'ARGS: {args}')
    logger.debug(f'JSON: {file[0].name}')
    shazam = Shazam(file[0].body)
    recognize_generator = shazam.recognizeSong()
    #logger.debug(type(recognize_generator))
    res = next(recognize_generator)  # current offset & shazam response to recognize requests
    #logger.debug(f'RESP: {res}')
    keysmapping = dict(subtitle='author', title='title')
    if 'track' in res[1]:
        res = {v: res[1]['track'][k] for k, v in keysmapping.items()}
    else:
        res = dict(msg="Unable to find a match")
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