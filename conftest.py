import pytest
import yaml
import logging

from library.api_client import APIClient
from library.services.cart_offer_services import CartOfferServices
from library.mockserver import MockServer
from library.util import Utils

def pytest_addoption(parser):
    parser.addoption(
        "--envfile",
        action="store",
        default=".local.env",
        help="Path to the .env file (default: .local.env)"
    )

@pytest.fixture(scope="session", autouse=True)
def load_env(pytestconfig):
    env_file = pytestconfig.getoption("envfile")
    Utils.set_env_config(env_file)

@pytest.fixture(scope="session")
def env_config():
    return Utils.get_env_config()

@pytest.fixture(scope="session")
def test_data():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

@pytest.fixture(scope="session")
def api_client(env_config):
    """Provides a shared API client across tests"""
    return APIClient(env_config["base_url"])

@pytest.fixture(scope="session")
def cart_offer(env_config) -> CartOfferServices:
    client = APIClient(env_config["base_url"])
    return CartOfferServices(client)

@pytest.fixture(scope="session")
def mockserver(env_config) -> MockServer:
    return MockServer(env_config["mockserver_url"])

def pytest_configure(config):
    cfg = Utils.get_env_config()
    config._metadata = {
        "Environment": cfg["env_name"],
        "Base URL": cfg["base_url"]
    }

def pytest_sessionstart(session):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    logging.info("📦 Pytest session started with environment config loaded.")
