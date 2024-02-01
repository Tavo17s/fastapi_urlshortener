from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from pydantic import BaseModel
from secrets import token_urlsafe

import json
import validators

app = FastAPI()
domain = 'http://127.0.0.1:8000'
fake_database = json.load(open('fake_database.json', 'r'))


class Url(BaseModel):
    url: str


@app.post('/short_url')
async def shorten_url(url: Url):
    url = url.url

    if validators.url(url):
        url_id = token_urlsafe(5)
        shortened_url = f'{domain}/{url_id}'
        fake_database['urls'].append({
            'url_id': url_id,
            'short_url': shortened_url,
            'target_url': url
        })
        json.dump(fake_database, open('fake_database.json', 'w'), indent=4)
        return {'msg': 'done', 'url': shortened_url}

    return {'msg': 'Invalid url'}


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get('/{_id}')
async def get_target_url(_id: str):
    for url in fake_database['urls']:
        if url['url_id'] == _id:
            return RedirectResponse(url['target_url'])

    return {'msg': 'Url not found'}
