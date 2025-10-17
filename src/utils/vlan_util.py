import json
import asyncio

from proxmoxer import ProxmoxAPI

from utils.util_interface import UtilInterface


class VlanUtil(UtilInterface):
    COMMAND = "vlan-audit"

    def __init__(self, proxmox: ProxmoxAPI, args):
        self.proxmox = proxmox
        self.args = args

    @staticmethod
    def add_arguments(sub_parsers):
        vlan_parser = sub_parsers.add_parser(
            VlanUtil.COMMAND,
            prog="Proxmox VLAN Auditor",
            description="Audit VLAN usage across VMs and containers",
            help="Audit VLAN usage"
        )
        vlan_parser.add_argument(
            "-m", "--mapping",
            choices=["vm", "vlan"],
            default="vm",
            help="The mapping to use. vm = VM to VLAN, vlan = VLAN to VM. Default: %(default)s"
        )
        vlan_parser.add_argument(
            "-o", "--output",
            choices=["text", "json", "csv"],
            default="text",
            help="The output format. text = default, json = JSON, csv = CSV. Default: %(default)s"
        )
        vlan_parser.add_argument(
            "-v", "--vlans",
            help="A comma-separated list of VLAN IDs to filter by. "
                 "Supplying this option defaults to vlan mapping (i.e., `--mapping vlan`)."
        )

    async def get_vm_info(self, node, vm_type, vm_id, name):
        if vm_type == "qemu":
            vm_config = self.proxmox.nodes(node).qemu(vm_id).config.get()
        elif vm_type == "lxc":
            vm_config = self.proxmox.nodes(node).lxc(vm_id).config.get()
        else:
            raise ValueError(f"Unknown VM type: {vm_type}")

        vlans = []
        for key, value in vm_config.items():
            if not key.startswith("net"):
                continue

            for net_configs in value.split(","):
                config = net_configs.split("=")
                if config[0] == "tag":
                    vlans.append(config[1])

        return {
            "name": name,
            "id": vm_id,
            "vlans": vlans
        }

    def print_vm_infos(self, vm_infos):
        match self.args.output:
            case "text":
                for vm_info in vm_infos:
                    print(f"{vm_info["id"]} ({vm_info["name"]}) -> {vm_info["vlans"]}")
            case "json":
                print(json.dumps(vm_infos, indent=2))
            case "csv":
                print("id,name,vlans")
                for vm_info in vm_infos:
                    print(f"{vm_info["id"]},{vm_info["name"]},[{",".join(vm_info["vlans"])}]")

    def get_vlan_infos(self, vm_infos):
        vlan_mapping = {}
        for vm_info in vm_infos:
            for vlan in vm_info["vlans"]:
                if vlan not in vlan_mapping:
                    vlan_mapping[vlan] = []
                vlan_mapping[vlan].append(f"{vm_info["id"]} ({vm_info["name"]})")
        return vlan_mapping

    def print_vlan_infos(self, vlan_mapping):
        match self.args.output:
            case "text":
                for vlan, vm_names in vlan_mapping.items():
                    print(f"{vlan} -> {vm_names}")
            case "json":
                print(json.dumps(vlan_mapping, indent=2))
            case "csv":
                print("vlan,vms")
                for vlan, vm_names in vlan_mapping.items():
                    print(f"{vlan},[{",".join(vm_names)}]")

    async def exec(self):
        futures = []
        for resource in self.proxmox.cluster.resources.get(type="vm"):
            vm_info_coroutine = self.get_vm_info(resource["node"], resource["type"],
                                                 resource["vmid"], resource["name"])
            future = asyncio.create_task(vm_info_coroutine)
            futures.append(future)

        vm_infos = await asyncio.gather(*futures)
        sorted_vm_infos = sorted(vm_infos, key=lambda info: info["id"])

        if self.args.vlans:
            vlans = self.args.vlans.split(",")
            vlan_infos = self.get_vlan_infos(sorted_vm_infos)
            filtered_vlan_infos = {vlan: vlan_infos[vlan] for vlan in vlans if vlan in vlan_infos}
            self.print_vlan_infos(filtered_vlan_infos)
        elif self.args.mapping == "vm":
            self.print_vm_infos(sorted_vm_infos)
        else:
            vlan_infos = self.get_vlan_infos(sorted_vm_infos)
            self.print_vlan_infos(vlan_infos)
