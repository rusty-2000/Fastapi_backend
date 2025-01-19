# allow us to read environment variables

from pydantic_settings import BaseSettings, SettingsConfigDict

class  Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET:str
    JWT_ALGORITHM:str
    REDIS_HOST :str="localhost"
    REDIS_PORT :int= 6379
    # openapi_url: str = ""

    model_config=SettingsConfigDict(env_file=".env", extra="ignore") # to change configuration in pydantic model
Config=Settings() # we don't have to create bew instance of setting

# rebuild_dataclass(
#     cls: type[PydanticDataclass],
#     *,
#     force: bool = False,
#     raise_errors: bool = True,
#     _parent_namespace_depth: int = 2,
#     _types_namespace: MappingNamespace | None = None
# ) -> bool | None