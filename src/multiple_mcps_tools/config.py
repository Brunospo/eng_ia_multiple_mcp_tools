import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
assert api_key, "OPENROUTER_API_KEY is not set in environment variables"


@dataclass
class ProviderSortConfig:
    by: str
    partition: str


@dataclass
class ProviderConfig:
    sort: ProviderSortConfig


@dataclass
class ModelConfig:
    api_key: str
    http_referer: str
    x_title: str
    provider: ProviderConfig
    models: list[str]
    temperature: float
    max_tokens: int


# Instanciando a configuração
config = ModelConfig(
    api_key=api_key,
    http_referer="",
    x_title="IA Devs - Transforming Services into Tools",
    models=["nvidia/nemotron-3.5-lightning:free"],
    provider=ProviderConfig(
        sort=ProviderSortConfig(
            by="throughput",
            partition="none",
        )
    ),
    temperature=0.7,
    max_tokens=100000,
)
