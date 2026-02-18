from typing import Optional

from applibs.status import VALID_DATA_NOT_FOUND, VALIDATION_ERROR_DICT

def format_output_success(response: dict, data: dict) -> dict:
    if data:
        response["data"] = data
    return response

def format_output_error(response: dict, error: str) -> dict:
    response["data"] = {}
    if error:
        response["error"] = error
    return response

def handle_validation_error(errors: dict) -> Optional[dict]:
    for error in errors.items():
        return error[1][0].code

    return None

def render_serializer_errors(errors: dict) -> dict:
    error_code = handle_validation_error(errors)
    return VALIDATION_ERROR_DICT.get(error_code, VALID_DATA_NOT_FOUND)