from typing import TypedDict

from ..models import Comment, ListComments
from .base import Resource


class CommentCreate(TypedDict):
    taskId: str
    content: str


class CommentListParams(TypedDict, total=False):
    cursor: str
    taskId: str


class CommentResource(Resource):
    base_path = "/comments"

    def create(self, data: CommentCreate) -> Comment:
        response = super().create(data)
        return Comment.model_validate(response.json())

    def list(self, params: CommentListParams | None = None) -> ListComments:
        response = super().list(params)
        return ListComments.model_validate(response.json())
