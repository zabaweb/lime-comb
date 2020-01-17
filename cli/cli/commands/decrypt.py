from dataclasses import dataclass
from cli.gpg import decrypt
from cli.config import Config
from cli.commands.base import Command


@dataclass
class DecryptCommand(Command):
    aliases: str = ("d", "dec")
    name: str = "decrypt"
    help: str = "Decrypt message"

    def __call__(self, msgs):
        for msg in msgs:
            decrypted_msg = decrypt(msg, always_trust=True, passphrase=Config.password)
            yield decrypted_msg
