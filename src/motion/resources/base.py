from abc import ABC

from requests import Response

from ..client import GenericTypedDict, HttpClient, HttpMethod


class Resource(ABC):
    """
    Base class for Motion API resources
    """

    base_path: str

    def __init__(self, client: HttpClient) -> None:
        self._client = client

        assert (
            self.base_path is not None
        ), "base_path must be defined on resource"

    def create(self, data: GenericTypedDict) -> Response:
        return self._client.call_api(
            HttpMethod.POST,
            self.base_path,
            data=data,
        )

    def update(self, object_id: str, data: GenericTypedDict) -> Response:
        return self._client.call_api(
            HttpMethod.PUT,
            path=f"{self.base_path}/{object_id}",
            data=data,
        )

    def delete(self, object_id: str) -> Response:
        return self._client.call_api(
            HttpMethod.DELETE,
            path=f"{self.base_path}/{object_id}",
        )

    def list(self, params: GenericTypedDict | None = None) -> Response:
        return self._client.call_api(
            HttpMethod.GET,
            path=self.base_path,
            params=params,  # type: ignore
        )

    def retrieve(self, object_id: str) -> Response:
        return self._client.call_api(
            HttpMethod.GET,
            path=f"{self.base_path}/{object_id}",
        )
