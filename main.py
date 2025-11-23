import secrets
from contextlib import asynccontextmanager

from fastapi import FastAPI, Query, Request
from fastapi.responses import PlainTextResponse, Response
from pydantic import BaseModel
from pydantic_extra_types.color import Color

from objects.embed import Embed
from services.db import DBService


@asynccontextmanager
async def lifespan(app: FastAPI):
    await DBService.init()
    yield
    await DBService.shutdown()


app = FastAPI(title="Discord embed api")


@app.get("/")
def index(request: Request):
    return {"docs": str(request.base_url) + "/docs"}


class EmbedModel(BaseModel):
    title: str = None
    author: str = None
    description: str = None
    image: str = None
    isImageThumbnail: bool
    color: Color = None


@app.post("/create")
async def create(embed: EmbedModel):
    cursor = await DBService.pool.execute(
        """
            INSERT INTO embeds
            (id, title, author, description, image, is_image_thumbnail, color)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            RETURNING *
        """,
        (
            secrets.token_hex(8),
            embed.title,
            embed.author,
            embed.description,
            embed.image,
            embed.isImageThumbnail,
            embed.color,
        ),
    )
    row = await cursor.fetchone()

    await DBService.pool.commit()

    return Embed.model_validate(dict(row))


def ogpTag(property: str, content: str):
    return f'<meta prefix="og: https://ogp.me/ns#" property="og:{property}" content="{content}"/>'


@app.get("/oembed")
def oembed(author: str = Query()):
    return {"type": "photo", "author_name": author}


@app.get("/e/{id:str}")
async def extract(request: Request, id: str):
    cursor = await DBService.pool.execute("SELECT * FROM embeds WHERE id = ?", (id,))
    row = await cursor.fetchone()

    if not row:
        return PlainTextResponse("404 Not found", 404)

    embed = Embed.model_validate(dict(row))

    metaTags = []

    if embed.title:
        metaTags.append(ogpTag("title", embed.title))
    if embed.description:
        metaTags.append(ogpTag("description", embed.description))
    if embed.author:
        metaTags.append(ogpTag("author", embed.author))
        metaTags.append(
            f'<link type="application/json+oembed" href="{request.base_url}/oembed?author={embed.author}"/>'
        )
    if embed.color:
        metaTags.append(f'<meta name="theme-color" content="{embed.color.as_hex()}"/>')
    if embed.image:
        if not embed.isImageThumbnail:
            metaTags.append('<meta name="twitter:card" content="summary_large_image"/>')
        metaTags.append(ogpTag("image", embed.image))

    return Response(
        f'<!DOCTYPE html><html><head><meta charset="UTF-8"/>{"".join(metaTags)}</head><body>embed</body></html>',
        media_type="text/html",
    )
