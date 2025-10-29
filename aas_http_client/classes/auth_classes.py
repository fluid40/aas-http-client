from pydantic import BaseModel, PrivateAttr, ValidationError


class BasicAuthConfig(BaseModel):
    username: str


class ServiceProviderAuthConfig(BaseModel):
    token_url: str
    client_id: str
    grant_type: str = "client_credentials"
    header_name: str = "Authorization"
    _client_secret: str = PrivateAttr(default=None)

    def set_client_secret(self, client_secret: str) -> None:
        self._client_secret = client_secret

    def get_client_secret(self) -> str:
        if self._client_secret is None:
            raise ValueError("Client secret has not been set.")
        return self._client_secret
