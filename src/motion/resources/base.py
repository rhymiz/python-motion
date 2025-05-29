from abc import ABC
from typing import Any, Generic, List, TypeVar

from pydantic import BaseModel

from ..client import GenericTypedDict, HttpClient, HttpMethod

# Type variables with proper bounds
CreateDataT = TypeVar("CreateDataT", bound=GenericTypedDict[Any])
UpdateDataT = TypeVar("UpdateDataT", bound=GenericTypedDict[Any])
ListParamsT = TypeVar("ListParamsT", bound=GenericTypedDict[Any])
ModelT = TypeVar("ModelT", bound=BaseModel)
ListModelT = TypeVar("ListModelT", bound=BaseModel)


class Resource(
    ABC, Generic[CreateDataT, UpdateDataT, ListParamsT, ModelT, ListModelT]
):
    """
    Base class for Motion API resources that return wrapped responses
    """

    base_path: str

    def __init__(self, client: HttpClient) -> None:
        self._client = client

        assert self.base_path is not None, (
            "base_path must be defined on resource"
        )

    def create(self, data: CreateDataT) -> ModelT:
        response = self._client.call_api(
            HttpMethod.POST,
            self.base_path,
            data=data,
        )
        return self._parse_model(response.json())

    def update(self, object_id: str, data: UpdateDataT) -> ModelT:
        response = self._client.call_api(
            HttpMethod.PUT,
            f"{self.base_path}/{object_id}",
            data=data,
        )
        return self._parse_model(response.json())

    def delete(self, object_id: str) -> None:
        self._client.call_api(
            HttpMethod.DELETE,
            f"{self.base_path}/{object_id}",
        )

    def list(self, params: ListParamsT | None = None) -> ListModelT:
        response = self._client.call_api(
            HttpMethod.GET,
            self.base_path,
            params=params,  # type: ignore
        )
        return self._parse_list_model(response.json())

    def retrieve(self, object_id: str) -> ModelT:
        response = self._client.call_api(
            HttpMethod.GET,
            f"{self.base_path}/{object_id}",
        )
        return self._parse_model(response.json())

    def _parse_model(self, data: Any) -> ModelT:
        """Override in subclasses to parse single model response"""
        raise NotImplementedError("Subclasses must implement _parse_model")

    def _parse_list_model(self, data: Any) -> ListModelT:
        """Override in subclasses to parse list model response"""
        raise NotImplementedError(
            "Subclasses must implement _parse_list_model"
        )


class SimpleListResource(ABC, Generic[ListParamsT, ModelT]):
    """
    Resource class for endpoints that return raw arrays instead of wrapped objects
    """

    base_path: str

    def __init__(self, client: HttpClient) -> None:
        self._client = client

        assert self.base_path is not None, (
            "base_path must be defined on resource"
        )

    def list(self, params: ListParamsT | None = None) -> List[ModelT]:
        response = self._client.call_api(
            HttpMethod.GET,
            self.base_path,
            params=params,  # type: ignore
        )
        return self._parse_list(response.json())

    def _parse_list(self, data: Any) -> List[ModelT]:
        """Override in subclasses to parse array response"""
        raise NotImplementedError("Subclasses must implement _parse_list")
