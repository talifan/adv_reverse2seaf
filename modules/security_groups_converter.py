# modules/security_groups_converter.py
import json
import ipaddress
from collections import defaultdict

from id_prefix import ensure_prefix, subnet_ref


def convert(source_data):
    """
    Converts Security Groups data to seaf.ta.services.kb format.
    """
    ensure_prefix(source_data=source_data)
    security_groups_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.security_groups', {})
    ecss_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.ecss', {}) or {}
    subnets_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.subnets', {}) or {}
    sg_to_subnets = defaultdict(set)
    subnet_networks = []

    for subnet_details in subnets_data.values():
        if not isinstance(subnet_details, dict):
            continue
        cidr = subnet_details.get('cidr')
        subnet_id = subnet_details.get('id')
        if not cidr or not subnet_id:
            continue
        try:
            network_obj = ipaddress.ip_network(cidr, strict=False)
        except ValueError:
            continue
        subnet_networks.append((network_obj, subnet_ref(subnet_id)))

    for ecs_details in ecss_data.values():
        if not isinstance(ecs_details, dict):
            continue
        subnet_ids = ecs_details.get('subnets') or []
        if not subnet_ids:
            continue
        linked_security_groups = ecs_details.get('security_groups') or []
        for sg_uuid in linked_security_groups:
            if not sg_uuid:
                continue
            for subnet_id in subnet_ids:
                if subnet_id:
                    sg_to_subnets[sg_uuid].add(subnet_ref(subnet_id))
    
    converted_kbs = {}
    
    for sg_id, sg_details in security_groups_data.items():
        new_id = sg_id
        
        description_parts = []
        if sg_details.get('description'):
            description_parts.append(sg_details.get('description'))
        if sg_details.get('tenant'):
            description_parts.append(f"Tenant: {sg_details.get('tenant')}")
        if sg_details.get('DC'):
            description_parts.append(f"DC: {sg_details.get('DC')}")

        rules = sg_details.get('rules', [])
        if rules:
            description_parts.append(f"Rules: {json.dumps(rules, indent=2)}")

        description = '\n'.join(description_parts).strip()
        network_refs = set(sg_to_subnets.get(sg_details.get('id'), set()))
        if not network_refs and subnet_networks:
            for rule in sg_details.get('rules', []) or []:
                prefix = rule.get('remote_ip_prefix')
                if not prefix:
                    continue
                try:
                    remote_net = ipaddress.ip_network(prefix, strict=False)
                except ValueError:
                    continue
                if remote_net.prefixlen < 16:
                    continue  # Skip overly broad networks
                for subnet_net, subnet_ref_id in subnet_networks:
                    if remote_net.version != subnet_net.version:
                        continue
                    if remote_net.subnet_of(subnet_net) or subnet_net.subnet_of(remote_net):
                        network_refs.add(subnet_ref_id)
        if not network_refs and subnet_networks:
            continue

        converted_kbs[new_id] = {
            'title': sg_details.get('name'),
            'description': description,
            'external_id': sg_details.get('id'),
            'technology': 'Межсетевое экранирование',
            'software_name': 'Cloud Security Group',
            'tag': 'FW',
            'status': 'Используется',
            'network_connection': sorted(network_refs),
        }

    return {'seaf.ta.services.kb': converted_kbs}
