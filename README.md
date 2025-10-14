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

### Environment

These utilities require certain environment variables to be set for authentication with your Proxmox server/cluster.

## Usage

For usage instructions, see `python proxmox_utils.py --help`.