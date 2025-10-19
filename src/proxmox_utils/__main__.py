# ruff: noqa: TID252
import asyncio
import os
import sys
from argparse import ArgumentParser

from dotenv import load_dotenv
from proxmoxer import ProxmoxAPI

from .utils.vlan_util import VlanUtil
from .utils.vm_info_util import VmInfoUtil

parser = ArgumentParser(
    prog="Proxmox Utilities", description="A set of utilities for working with Proxmox VE deployments"
)
parser.add_argument(
    "-e",
    "--env",
    help="Path to a .env file to load environment variables from. " "Defaults to .env in the current directory.",
)
sub_parsers = parser.add_subparsers(dest="command", help="Subcommand help")
VmInfoUtil.add_arguments(sub_parsers)
VlanUtil.add_arguments(sub_parsers)

args = parser.parse_args()

proxmox: ProxmoxAPI


async def main():
    if args.env:
        load_dotenv(dotenv_path=args.env)
    else:
        load_dotenv()

    host = _get_env_var("PVE_HOST")
    user = _get_env_var("PVE_USER")
    token_name = _get_env_var("PVE_TOKEN_NAME")
    token_value = _get_env_var("PVE_TOKEN_VALUE")

    proxmox = ProxmoxAPI(host=host, user=user, token_name=token_name, token_value=token_value, verify_ssl=False)

    match args.command:
        case VmInfoUtil.COMMAND:
            vm_info_util = VmInfoUtil(proxmox, args)
            await vm_info_util.exec()
        case VlanUtil.COMMAND:
            vlan_util = VlanUtil(proxmox, args)
            await vlan_util.exec()
        case _:
            parser.print_help()


def _get_env_var(var_name: str):
    value = os.getenv(var_name)
    if value is None:
        print(f"{var_name} environment variable is not set. Exiting.")
        sys.exit(1)
    else:
        return value


asyncio.run(main())
