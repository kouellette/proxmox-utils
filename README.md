# Proxmox Utils

A collection of utilities for interacting with Proxmox Virtual Environment (PVE) servers.

## Setup

### Packages

To use these utilities, you need Python installed and need to install the required packages. The recommended way
is to use a virtual environment. `venv` is the built-in virtual environment manager so the following example uses it,
but you can replace it with your favorite virtual environment manager.

```bash
# Create a virtual environment in a folder named 'venv'
python3 -m venv venv
# Activate the virtual environment 
source venv/bin/activate
# Install the required packages
pip install -r requirements.txt
```

### Proxmox API Token

To authenticate with your Proxmox server/cluster, an API token needs to be created. API Tokens can be created from the
Datacenter -> Permissions -> API Tokens tab in the Proxmox web interface. For fine-grained permission control of the token,
[this blog](https://kenwardtown.com/2024/06/25/create-an-api-token-for-proxmox-ve/https://kenwardtown.com/2024/06/25/create-an-api-token-for-proxmox-ve/)
provides a good overview.

After creating the token, take note of the username associated with the token, the token name/ID, and of course the token
secret. These will be needed to set the environment variables below.

### Environment

These utilities require certain environment variables to be set for authentication with your Proxmox server/cluster.
The following environment variables must be set before running the utilities:

- `PVE_HOST`: The hostname or IP address of the Proxmox server/cluster to connect to.
- `PVE_USER`: The username associated with the API token.
- `PVE_TOKEN_NAME`: The name/ID of the API Token created in the Proxmox web interface.
- `PVE_TOKEN_VALUE`: The secret value of the API Token.

You can set these environment variables in your shell or add them to a `.env` file in the root of the project.
For convenience, you can copy the provided `.env.template` file to `.env` and fill in the required values.

```bash

## Usage

For usage instructions, see `python proxmox_utils.py --help`.