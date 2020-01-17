import pytest
from cli.gpg import geneate_keys, encrypt
import tempfile
import os
from cli.config import Config


@pytest.yield_fixture(autouse=True)
def temp_data_dir():
    data_dir = tempfile.mkdtemp()
    Config.data_dir = data_dir
    yield data_dir
    os.rmdir(data_dir)


@pytest.fixture
def keypair(temp_data_dir):
    keys = geneate_keys()
    return keys.fingerprint


def test_encrypt(keypair):
    enc_msg = encrypt(Config.email, "test data")
    assert enc_msg.startswith("-----BEGIN PGP MESSAGE----")


def test_decrypt():
    pass  # TODO


def test_generate_keypair():
    keys = geneate_keys()
    assert keys.fingerprint
