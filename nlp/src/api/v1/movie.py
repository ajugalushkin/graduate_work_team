"""Movie endpoints."""

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from src.core import Container
from src.services import NLPSearchService


router = APIRouter()

@router.get(
    "/query",
    summary="Get info by text query",
    description="Return information text query",
)
@inject
async def get_by_query(
    query: str,
    nlp_search_service: NLPSearchService = Depends(
        Provide[Container.nlp_search_service]
    ),
):
    data = await nlp_search_service.parse_query(query=query)
    if not data:
        raise HTTPException(status_code=204, detail="Info not found")
    return data

@router.get(
    "/pattern",
    summary="Get info by pattern query",
    description="Return information pattern query",
)
@inject
async def get_by_pattern(
    query: str,
    nlp_search_service: NLPSearchService = Depends(
        Provide[Container.nlp_search_service]
    ),
):
    data = await nlp_search_service.search_by_pattern(query=query)
    if not data:
        raise HTTPException(status_code=204, detail="Info not found")
    return data

@router.get(
    "/{movie_id}",
    summary="Get movie data",
    description="Return full movie information by id",
)
@inject
async def get_movie(
    movie_id: str,
    nlp_search_service: NLPSearchService = Depends(
        Provide[Container.nlp_search_service]
    ),
):
    data = await nlp_search_service.get_by_id(movie_id)
    if not data:
        raise HTTPException(status_code=204, detail="Movie not found")
    return data
