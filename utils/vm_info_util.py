import re
import json

from proxmoxer import ProxmoxAPI
from proxmoxer import ResourceException

from utils.UtilInterface import UtilInterface


class VmInfoUtil(UtilInterface):
    COMMAND = "get-vm-info"
    NODE_FIELD = "node"
    VMID_FIELD = "vmid"
    NAME_FIELD = "name"
    UUID_FIELD = "vmgenid"

    def __init__(self, proxmox: ProxmoxAPI, args):
        self.proxmox = proxmox
        self.args = args

    @staticmethod
    def add_arguments(sub_parsers):
        uuid_parser = sub_parsers.add_parser(
            VmInfoUtil.COMMAND,
            prog="Proxmox VM Info Getter",
            description="A program for getting info of a VM on a Proxmox VE server",
            help="Get info of a VM on a Proxmox VE server"
        )

        group = uuid_parser.add_mutually_exclusive_group(required=True)
        group.add_argument("-n", "--name", help="The name of the VM")
        group.add_argument("-i", "--id", help="The ID of the VM")

        uuid_parser.add_argument(
            "-u", "--uuid",
            action="store_true",
            help="Return only the VM's UUID"
        )

    async def exec(self):
        try:
            vm = None
            if self.args.id:
                vm = self.find_vm_by_id(int(self.args.id))
            elif self.args.name:
                vm = self.find_vm_by_name(self.args.name)

            if vm is None:
                if self.args.id:
                    print(f"VM with ID [{self.args.id}] not found")
                elif self.args.name:
                    print(f"VM with name [{self.args.name}] not found")
                return

            config = (
                self.proxmox
                .nodes(vm[VmInfoUtil.NODE_FIELD])
                .qemu(vm[VmInfoUtil.VMID_FIELD])
                .config
                .get()
            )
            if self.args.uuid:
                print(config.get(VmInfoUtil.UUID_FIELD, "VM UUID not found"))
            else:
                print(json.dumps(config, indent=2))
        except ResourceException as exception:
            print(exception)
            if re.match("Configuration file .* does not exist", exception.content):
                print("Hint: This error likely means that the resource with the provided "
                      "ID/name is an LXC rather than a VM.")
        except ValueError:
            print(f"Invalid VM ID [{self.args.id}]. Must be a number")

    def _get_vms(self):
        return self.proxmox.cluster.resources.get(type="vm")

    def find_vm_by_id(self, vm_id):
        vms = self._get_vms()
        return next((vm for vm in vms if vm[VmInfoUtil.VMID_FIELD] == vm_id), None)

    def find_vm_by_name(self, name):
        vms = self._get_vms()
        return next((vm for vm in vms if vm[VmInfoUtil.NAME_FIELD] == name), None)
