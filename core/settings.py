from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    environment: str = "development"

    # Azure OpenAI settings
    azure_openai_api_key: str = ""
    azure_openai_endpoint: str = ""
    azure_openai_deployment_name: str = "gpt-4"

    # Azure Vision settings
    azure_vision_api_key: str = ""
    azure_vision_endpoint: str = ""

    @property
    def is_development(self) -> bool:
        return self.environment == "development"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
