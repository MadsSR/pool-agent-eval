from paramiko import SSHClient, AutoAddPolicy, SFTPClient
from dotenv import load_dotenv
import os


def get_sftp_client() -> SFTPClient:
    load_dotenv()
    SSH_HOSTNAME = os.getenv("SSH_HOSTNAME")
    SSH_USER = os.getenv("SSH_USER")
    SSH_ID_FILE = os.path.expanduser(os.getenv("SSH_ID_FILE"))
    SSH_KEY_PASSPHRASE = os.getenv("SSH_KEY_PASSPHRASE")

    ssh_client = SSHClient()
    ssh_client.set_missing_host_key_policy(AutoAddPolicy())
    ssh_client.connect(SSH_HOSTNAME, username=SSH_USER,
                       key_filename=SSH_ID_FILE, passphrase=SSH_KEY_PASSPHRASE)
    sftp_client = ssh_client.open_sftp()
    return sftp_client


def fetch_model(model_name: str):
    client = get_sftp_client()
    client.get(f"pool/models/{model_name}", f"models/{model_name}")
    client.close()


def list_models():
    client = get_sftp_client()
    models = client.listdir("pool/models")
    client.close()
    return models
