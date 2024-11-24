# objectid_str.py
from typing import Annotated, Any, Callable
from bson import ObjectId


def custom_json_encoder(obj: Any) -> Any:
    if isinstance(obj, ObjectId):
        return str(obj)  # Chuyển đổi ObjectId thành str
    if isinstance(obj, list):
        return [custom_json_encoder(item) for item in obj]  # Xử lý danh sách
    return obj  # Giữ nguyên
