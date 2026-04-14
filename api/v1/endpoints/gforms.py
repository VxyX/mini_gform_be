from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import PlainTextResponse
import requests
import re
import json
from bs4 import BeautifulSoup
import httpx

router = APIRouter()

def _map_type_name(code: int) -> str:
    # Matches your Dart QuestionType enum names
    mapping = {
        0: "text",
        1: "paragraph",
        2: "multipleChoice",
        3: "dropdown",
        4: "checkboxes",
        9: "date",
        10: "time",
        8: "sectionHeader"
    }
    return mapping.get(code, "unsupported")

@router.get("/parse")
async def parse_google_form(url: str = Query(...)):
    try:
        async with httpx.AsyncClient() as client:
            # We use a real User-Agent to ensure Google returns the full HTML form
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = await client.get(url, headers=headers, follow_redirects=True)
            
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Failed to fetch form")
            
            # Return the raw HTML as plain text
            return PlainTextResponse(content=response.text)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))