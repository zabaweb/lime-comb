import ast
import tempfile
from pathlib import Path
from unittest.mock import PropertyMock, patch
from uuid import uuid4

import lime_comb
import lime_comb.config
import lime_comb.firestore.database
import pyperclip
import pytest
import requests_mock
from lime_comb.auth.google import get_anon_cred
from lime_comb.gpg import delete_gpg_key, geneate_keys, gpg_engine
from mockfirestore.client import MockFirestore
from yaml import dump


@pytest.yield_fixture
def cred():
    with get_anon_cred() as c:
        yield c


@pytest.fixture
def domain():
    return "example.com"


@pytest.fixture
def mocked_resp():
    return '{"some": "response"}'


@pytest.yield_fixture
def oauth_gcp_conf(mocked_resp, oauth_client_config):
    with requests_mock.Mocker(real_http=True) as m:
        m.register_uri(
            "GET", lime_comb.config.config.client_lime_comb_url, text=mocked_resp
        )
        yield


@pytest.yield_fixture
def temp_file():
    with tempfile.NamedTemporaryFile() as fp:
        yield fp


@pytest.fixture
def key_id(uuid):
    return uuid


@pytest.fixture
def uuid():
    return str(uuid4())


class Creds:
    def __init__(self, uuid, expired=True):
        self.expired = expired
        self.uuid = uuid


@pytest.fixture
def valid_cred(uuid):
    return Creds(expired=False, uuid=uuid)


@pytest.yield_fixture(autouse=True)
def credentials_file(mocker, config_file, uuid):
    path = Path(f"{lime_comb.config.config.credentials_file}.test-{uuid}")
    with patch(
        "lime_comb.config.Config.credentials_file", new_callable=PropertyMock
    ) as credentials_file_mock:
        credentials_file_mock.return_value = path
        yield


@pytest.yield_fixture(autouse=True)
def oauth_client_config(mocker, config_file, uuid):
    path = Path(f"{lime_comb.config.config.oauth_client_config}.test-{uuid}")
    with patch(
        "lime_comb.config.Config.oauth_client_config", new_callable=PropertyMock
    ) as password_mock:
        password_mock.return_value = path
        yield


@pytest.yield_fixture(autouse=True)
def email(mocker, config_file):
    _email = "example.example@example.com"
    with patch(
        "lime_comb.config.Config.email", new_callable=PropertyMock
    ) as password_mock:
        password_mock.return_value = _email
        yield _email


@pytest.yield_fixture(autouse=True)
def config_dir(mocker, config_file):
    with tempfile.TemporaryDirectory() as dir_name:
        with patch(
            "lime_comb.config.Config.config_dir", new_callable=PropertyMock
        ) as config_dir_mock:
            config_dir_mock.return_value = Path(dir_name)
            yield dir_name


@pytest.yield_fixture(autouse=True)
def config_file(mocker, temp_file):
    with patch(
        "lime_comb.config.Config.config_file", new_callable=PropertyMock
    ) as config_file_mock:
        config_file_mock.return_value = Path(temp_file.name)
        yield temp_file.name


@pytest.fixture
def existing_config(config_file, email):
    with open(config_file, "w") as f:
        f.write(dump({"email": email}))


@pytest.yield_fixture
def password(mocker, config_file):
    _password = "dupa.8Polska12"
    with patch(
        "lime_comb.config.Config.password", new_callable=PropertyMock
    ) as password_mock:
        password_mock.return_value = _password
        yield _password


@pytest.yield_fixture
def username(mocker, config_file):
    _username = "example"
    with patch(
        "lime_comb.config.Config.username", new_callable=PropertyMock
    ) as username_mock:
        username_mock.return_value = _username
        yield _username


@pytest.fixture
def invalid_cred(uuid):
    return Creds(uuid=uuid)


@pytest.yield_fixture()
def pyperclip_copy(mocker):
    mocker.patch.object(pyperclip, "copy")
    yield


@pytest.yield_fixture
def web_login(mocker, uuid):
    mocker.patch.object(
        lime_comb.auth.google, "web_login", return_value=Creds(expired=False, uuid=uuid)
    )
    yield


def fake_list_gpg_ids(key_id):
    def list_gpg_ids(*args, **kwargs):
        yield key_id

    return list_gpg_ids


@pytest.yield_fixture()
def mocked_db(key_id, valid_cred, mocker):
    db = MockFirestore()
    mocker.patch.object(
        lime_comb.firestore.database, "get_firestore_db", return_value=db
    )
    mocker.patch.object(
        lime_comb.firestore.database,
        "list_gpg_ids",
        return_value=fake_list_gpg_ids(key_id)(),
    )
    yield db
    db.reset()


@pytest.yield_fixture
def mocked_gpg_key(mocked_db, key_id, email, domain, priv_key, pub_key):
    mocked_db.collection(domain).document(f"{email}/{key_id}/priv").set(
        {"data": priv_key}
    )
    mocked_db.collection(domain).document(f"{email}/{key_id}/pub").set(
        {"data": pub_key}
    )
    yield f"{key_id}"


@pytest.yield_fixture
def keypair(mocker, password, username):
    keys = geneate_keys()
    pub = gpg_engine().export_keys(keys.fingerprint)
    priv = gpg_engine().export_keys(keys.fingerprint, True, passphrase=password)
    yield pub, priv, keys.fingerprint
    delete_gpg_key(keys.fingerprint, lime_comb.config.config.password)


@pytest.fixture
def priv_key(keypair):
    return keypair[1]


@pytest.fixture
def pub_key(keypair):
    return keypair[0]
