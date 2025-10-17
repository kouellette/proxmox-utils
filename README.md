# Proxmox Utils

A collection of utilities for interacting with Proxmox Virtual Environment (PVE) servers via the [Proxmox API](https://pve.proxmox.com/wiki/Proxmox_VE_API).
Because of this, these utilities can be run from any machine that has connectivity to the Proxmox server/cluster. 

## Setup

### Packages

To use these utilities, you need Python installed and need to install the required packages. The recommended way
is to use a virtual environment. `venv` is the built-in virtual environment manager, so the following example uses it, 
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
Datacenter → Permissions → API Tokens tab in the Proxmox web interface. For fine-grained permission control of the token,
[this blog](https://kenwardtown.com/2024/06/25/create-an-api-token-for-proxmox-ve/https://kenwardtown.com/2024/06/25/create-an-api-token-for-proxmox-ve/)
provides a good overview.

After creating the token, take note of the username associated with the token, the token name/ID, and token secret. 
These will be needed to set the environment variables below.

### Environment

These utilities require certain environment variables to be set for authentication with your Proxmox server/cluster.
The following environment variables must be set before running the utilities:

- `PVE_HOST`: The hostname or IP address of the Proxmox server/cluster to connect to.
- `PVE_USER`: The username associated with the API token.
- `PVE_TOKEN_NAME`: The name/ID of the API Token created in the Proxmox web interface.
- `PVE_TOKEN_VALUE`: The secret value of the API Token.

You can set these environment variables in your shell or add them to a file named `.env` in the root of the project.
For convenience, you can copy the provided `.env.template` file to `.env` and fill in the required values.

## Usage

```aiignore
usage: Proxmox Utilities [-h] {get-vm-info,vlan-audit} ...

A set of utilities for working with Proxmox VE deployments

positional arguments:
  {get-vm-info,vlan-audit}
                        Subcommand help
    get-vm-info         Get VM info
    vlan-audit          Audit VLAN usage

options:
  -h, --help            show this help message and exit
```

### Utilities

### `get-vm-info`

```aiignore
usage: Proxmox VM Info Getter [-h] (-n NAME | -i ID) [-u]

Get information on a specified VM

options:
  -h, --help       show this help message and exit
  -n, --name NAME  The name of the VM
  -i, --id ID      The ID of the VM
  -u, --uuid       Return only the VM's UUID
```

### `vlan-audit`

```aiignore
usage: Proxmox VLAN Auditor [-h] [-m {vm,vlan}] [-o {text,json,csv}] [-v VLANS]

Audit VLAN usage across VMs and containers

options:
  -h, --help            show this help message and exit
  -m, --mapping {vm,vlan}
                        The mapping to use. vm = VM to VLAN, vlan = VLAN to VM. Default: vm
  -o, --output {text,json,csv}
                        The output format. text = default, json = JSON, csv = CSV. Default: text
  -v, --vlans VLANS     A comma-separated list of VLAN IDs to filter by. Supplying this option defaults to vlan mapping (i.e., `--mapping vlan`).
```
