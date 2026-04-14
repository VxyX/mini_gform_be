from fastapi import APIRouter, HTTPException, Query
import requests
import re
import json
from bs4 import BeautifulSoup

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
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to load form")
        
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # Extracting tokens and IDs [cite: 5, 6]
        fbzx_match = re.search(r'name="fbzx" value="([^"]+)"', html)
        fbzx_token = fbzx_match.group(1) if fbzx_match else None
        
        id_match = re.search(r'/forms/d/e/([^/]+)/', url)
        form_id = id_match.group(1) if id_match else ""

        # Extract JSON data from script [cite: 7, 8]
        script_tags = soup.find_all('script')
        json_str = None
        for script in script_tags:
            if script.string and 'FB_PUBLIC_LOAD_DATA_' in script.string:
                match = re.search(r'FB_PUBLIC_LOAD_DATA_ = (\[.*?\]);', script.string, re.DOTALL)
                if match:
                    json_str = match.group(1)
                    break

        if not json_str:
            raise HTTPException(status_code=404, detail="Form data not found")

        data = json.loads(json_str) # [cite: 9]
        
        form_title = data[1][8] or 'Google Form' # [cite: 9, 10]
        description = data[1][0] or ''
        
        pages = []
        current_questions = []
        current_page_title = None

        for item in data[1][1]: # [cite: 11]
            q_title = item[1] or ''
            type_code = item[3] or -1 # [cite: 12]
            q_type = _map_type_name(type_code)

            if q_type == "sectionHeader": # [cite: 13]
                pages.append({
                    "title": current_page_title,
                    "description": "", # Placeholder for page description
                    "questions": current_questions
                })
                current_questions = []
                current_page_title = q_title
                continue

            q_payload = item[4] # [cite: 15]
            if not q_payload: continue
            
            q_inner = q_payload[0]
            q_id = str(q_inner[0]) if q_inner[0] else "" # [cite: 17]
            
            # Options [cite: 18, 19]
            options = None
            if q_type in ["multipleChoice", "dropdown", "checkboxes"] and len(q_inner) > 1:
                options_data = q_inner[1]
                if options_data:
                    options = [str(o[0]) for o in options_data if o[0]]

            # Validation logic [cite: 20-33]
            validation = None
            if len(q_inner) > 4 and q_inner[4]:
                v_data = q_inner[4][0]
                if isinstance(v_data, list) and len(v_data) >= 3:
                    v_type = "number" if v_data[0] == 1 else "none"
                    v_params = v_data[2]
                    validation = {
                        "type": v_type,
                        "min": float(v_params[0]) if v_data[1] in [7, 2] and v_params else None,
                        "max": float(v_params[1]) if v_data[1] == 7 and len(v_params) > 1 else (float(v_params[0]) if v_data[1] == 4 else None),
                        "errorMessage": v_data[3] if len(v_data) > 3 else None
                    }

            current_questions.append({
                "id": q_id,
                "title": q_title,
                "helpText": item[2] or None, # Mapping help text
                "type": q_type,
                "options": options,
                "isRequired": q_inner[2] == 1,
                "validation": validation
            })

        # Add last page [cite: 36, 37]
        pages.append({
            "title": current_page_title,
            "description": "",
            "questions": current_questions
        })

        return {
            "title": form_title,
            "description": description,
            "formId": form_id,
            "fbzxToken": fbzx_token,
            "pages": pages
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))