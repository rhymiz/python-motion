from typing import Any, NotRequired, Required

from ..client import GenericTypedDict
from ..models import Comment, ListComments
from .base import Resource


class CommentCreateData(GenericTypedDict[Any]):
    taskId: Required[str]
    content: Required[str]


class CommentListParams(GenericTypedDict[Any]):
    taskId: Required[str]
    cursor: NotRequired[str]


class CommentResource(
    Resource[
        CommentCreateData,
        CommentCreateData,
        CommentListParams,
        Comment,
        ListComments,
    ]
):
    base_path = "/comments"

    def _parse_model(self, data: Any) -> Comment:
        return Comment.model_validate(data)

    def _parse_list_model(self, data: Any) -> ListComments:
        return ListComments.model_validate(data)
