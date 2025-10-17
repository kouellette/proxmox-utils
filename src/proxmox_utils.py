import os
import asyncio

from argparse import ArgumentParser
from dotenv import load_dotenv
from utils.vm_info_util import VmInfoUtil
from utils.vlan_util import VlanUtil
from proxmoxer import ProxmoxAPI

parser = ArgumentParser(
    prog="Proxmox Utilities",
    description="A set of utilities for working with Proxmox VE deployments"
)
sub_parsers = parser.add_subparsers(dest="command", help="Subcommand help")
VmInfoUtil.add_arguments(sub_parsers)
VlanUtil.add_arguments(sub_parsers)

args = parser.parse_args()

proxmox: ProxmoxAPI


async def main():
    load_dotenv()

    host = os.getenv("PVE_HOST")
    user = os.getenv("PVE_USER")
    token_name = os.getenv("PVE_TOKEN_NAME")
    token_value = os.getenv("PVE_TOKEN_VALUE")

    global proxmox
    proxmox = ProxmoxAPI(host=host, user=user, token_name=token_name,
                         token_value=token_value, verify_ssl=False)

    match args.command:
        case VmInfoUtil.COMMAND:
            vm_info_util = VmInfoUtil(proxmox, args)
            await vm_info_util.exec()
        case VlanUtil.COMMAND:
            vlan_util = VlanUtil(proxmox, args)
            await vlan_util.exec()
        case _:
            parser.print_help()

asyncio.run(main())
