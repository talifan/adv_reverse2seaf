from collections import defaultdict
import re

from id_prefix import ensure_prefix


def _iter_values(value):
    if value is None:
        return []
    if isinstance(value, str):
        cleaned = value.strip()
        return [cleaned] if cleaned else []
    if isinstance(value, (list, tuple, set)):
        results = []
        for item in value:
            if isinstance(item, str):
                cleaned = item.strip()
                if cleaned:
                    results.append(cleaned)
        return results
    return []


def _id_variants(identifier):
    variants = set()
    if not identifier or not isinstance(identifier, str):
        return variants
    cleaned = identifier.strip()
    if not cleaned:
        return variants
    variants.add(cleaned)
    if '.' in cleaned:
        variants.add(cleaned.split('.')[-1])
    return variants


class LocationResolver:
    """
    Helper for inferring DC identifiers (e.g. 'ru-moscow-1a') for various resources based on
    hints contained in the raw reverse-engineering dataset.
    """

    def __init__(self, source_data):
        self.prefix = ensure_prefix(source_data=source_data)
        self.subnet_hints = defaultdict(set)  # subnet_id -> {dc_name}
        self.vpc_hints = defaultdict(set)     # vpc_id -> {dc_name}
        self.dc_aliases = defaultdict(set)    # dc_name -> {alias_dc_names}
        self._collect_hints(source_data or {})

    INVALID_DC_TOKENS = (
        'идентификатор',
        'суности',
        'placeholder',
    )

    _VALID_DC_PATTERN = re.compile(r'^[A-Za-z0-9_.-]+$')

    def _normalize_dc(self, value):
        if not value or not isinstance(value, str):
            return None
        cleaned = value.strip()
        if not cleaned:
            return None
        prefix_token = f"{self.prefix}.dc."
        candidate = cleaned
        if cleaned.startswith(prefix_token):
            candidate = cleaned[len(prefix_token):]
        elif '.dc.' in cleaned:
            candidate = cleaned.split('.dc.', 1)[1]
        elif cleaned.startswith('dc.'):
            candidate = cleaned.split('dc.', 1)[1]
        if not self._is_valid_dc_name(candidate):
            return None
        return candidate

    def _is_valid_dc_name(self, name):
        if not name:
            return False
        normalized = name.strip()
        if not normalized:
            return False
        lowered = normalized.lower()
        if any(token in lowered for token in self.INVALID_DC_TOKENS):
            return False
        if any(ch.isspace() for ch in normalized):
            return False
        if '/' in normalized:
            return False
        if not any(ch.isdigit() for ch in normalized):
            return False
        if not self._VALID_DC_PATTERN.match(normalized):
            return False
        return True

    def is_valid_dc_name(self, name):
        return self._is_valid_dc_name(name)

    def _register_alias(self, primary, secondary):
        primary_candidates = [_val for val in _iter_values(primary) if (_val := self._normalize_dc(val))]
        secondary_candidates = [_val for val in _iter_values(secondary) if (_val := self._normalize_dc(val))]
        for primary_value in primary_candidates:
            for secondary_value in secondary_candidates:
                if primary_value != secondary_value:
                    self.dc_aliases[primary_value].add(secondary_value)

    def _register_subnet_hint(self, subnet_id, hint):
        if not subnet_id:
            return
        for value in _iter_values(hint):
            normalized = self._normalize_dc(value)
            if not normalized:
                continue
            for key in _id_variants(subnet_id):
                self.subnet_hints[key].add(normalized)

    def _register_vpc_hint(self, vpc_id, hint):
        if not vpc_id:
            return
        for value in _iter_values(hint):
            normalized = self._normalize_dc(value)
            if not normalized:
                continue
            for key in _id_variants(vpc_id):
                self.vpc_hints[key].add(normalized)

    def _collect_hints(self, source_data):
        subnets_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.subnets', {}) or {}
        for subnet_key, details in subnets_data.items():
            subnet_id = details.get('id') or subnet_key
            self._register_subnet_hint(subnet_id, details.get('availability_zone'))
            self._register_subnet_hint(subnet_id, details.get('az'))
            self._register_subnet_hint(subnet_id, details.get('DC'))
            self._register_alias(details.get('DC'), details.get('availability_zone'))
            self._register_alias(details.get('DC'), details.get('az'))

        vpcs_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.vpcs', {}) or {}
        for vpc_key, details in vpcs_data.items():
            vpc_id = details.get('id') or vpc_key
            self._register_vpc_hint(vpc_id, details.get('DC'))

        ecss_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.ecss', {}) or {}
        for ecs_details in ecss_data.values():
            vpc_id = ecs_details.get('vpc_id')
            ecs_dc = ecs_details.get('DC')
            ecs_az = ecs_details.get('az')
            self._register_vpc_hint(vpc_id, ecs_az)
            self._register_vpc_hint(vpc_id, ecs_dc)
            self._register_alias(ecs_dc, ecs_az)

            for subnet_id in ecs_details.get('subnets') or []:
                self._register_subnet_hint(subnet_id, ecs_az)
                self._register_subnet_hint(subnet_id, ecs_dc)

            for disk_item in ecs_details.get('disks') or []:
                if isinstance(disk_item, dict):
                    for disk_props in disk_item.values():
                        self._register_alias(ecs_dc, disk_props.get('az'))
                        for subnet_id in ecs_details.get('subnets') or []:
                            self._register_subnet_hint(subnet_id, disk_props.get('az'))

        cces_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.cces', {}) or {}
        for cce_details in cces_data.values():
            vpc_id = cce_details.get('vpc_id')
            subnet_id = cce_details.get('subnet_id')
            masters_az = cce_details.get('masters_az')
            cce_dc = cce_details.get('DC')
            self._register_vpc_hint(vpc_id, masters_az)
            self._register_vpc_hint(vpc_id, cce_dc)
            self._register_alias(cce_dc, masters_az)
            self._register_subnet_hint(subnet_id, masters_az)
            self._register_subnet_hint(subnet_id, cce_dc)

        rdss_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.rdss', {}) or {}
        for rds_details in rdss_data.values():
            vpc_id = rds_details.get('vpc_id')
            subnet_id = rds_details.get('subnet_id')
            az = rds_details.get('az')
            rds_dc = rds_details.get('DC')
            self._register_vpc_hint(vpc_id, az)
            self._register_vpc_hint(vpc_id, rds_dc)
            self._register_alias(rds_dc, az)
            self._register_subnet_hint(subnet_id, az)
            self._register_subnet_hint(subnet_id, rds_dc)

        dmss_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.dmss', {}) or {}
        for dms_details in dmss_data.values():
            vpc_id = dms_details.get('vpc_id')
            subnet_id = dms_details.get('subnet_id')
            available_az = dms_details.get('available_az')
            dms_dc = dms_details.get('DC')
            self._register_vpc_hint(vpc_id, available_az)
            self._register_vpc_hint(vpc_id, dms_dc)
            self._register_alias(dms_dc, available_az)
            self._register_subnet_hint(subnet_id, available_az)
            self._register_subnet_hint(subnet_id, dms_dc)

        nat_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.nat_gateways', {}) or {}
        for nat_details in nat_data.values():
            subnet_id = nat_details.get('subnet_id')
            az = nat_details.get('availability_zone')
            nat_dc = nat_details.get('DC')
            self._register_subnet_hint(subnet_id, az)
            self._register_subnet_hint(subnet_id, nat_dc)
            self._register_alias(nat_dc, az)

        elb_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.elbs', {}) or {}
        for elb_details in elb_data.values():
            subnet_id = elb_details.get('subnet_id')
            az = elb_details.get('availability_zone')
            elb_dc = elb_details.get('DC')
            self._register_subnet_hint(subnet_id, az)
            self._register_subnet_hint(subnet_id, elb_dc)
            self._register_alias(elb_dc, az)

        vpn_gw_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.vpn_gateways', {}) or {}
        for vpn_details in vpn_gw_data.values():
            subnet_id = vpn_details.get('subnet_id')
            az = vpn_details.get('availability_zone')
            vpn_dc = vpn_details.get('DC')
            self._register_subnet_hint(subnet_id, az)
            self._register_subnet_hint(subnet_id, vpn_dc)
            self._register_alias(vpn_dc, az)

        eips_data = source_data.get('seaf.ta.reverse.cloud_ru.advanced.eips', {}) or {}
        for eip_details in eips_data.values():
            eip_dc = eip_details.get('DC')
            self._register_alias(eip_dc, eip_details.get('availability_zone'))

    def _expand_candidates(self, direct_candidates):
        expanded = set(direct_candidates)
        queue = list(direct_candidates)
        while queue:
            current = queue.pop()
            for alias in self.dc_aliases.get(current, ()):
                if alias not in expanded:
                    expanded.add(alias)
                    queue.append(alias)
        return expanded

    @staticmethod
    def _score_candidate(name, direct_candidates):
        score = 0
        if name in direct_candidates:
            score += 10
        if name and any(ch.isalpha() for ch in name):
            score += 3
        if name and '-' in name:
            score += 1
        if name and name.isdigit():
            score -= 2
        return score

    def _pick_best(self, direct_candidates):
        if not direct_candidates:
            return None
        expanded = self._expand_candidates(direct_candidates)
        sorted_candidates = sorted(
            expanded,
            key=lambda item: (-self._score_candidate(item, direct_candidates), item)
        )
        return sorted_candidates[0] if sorted_candidates else None

    def get_dc_for_subnet(self, subnet_id):
        direct = set()
        for key in _id_variants(subnet_id):
            direct.update(self.subnet_hints.get(key, ()))
        return self._pick_best(direct)

    def get_dc_names_for_vpc(self, vpc_id):
        direct = set()
        for key in _id_variants(vpc_id):
            direct.update(self.vpc_hints.get(key, ()))
        if not direct:
            return []
        expanded = self._expand_candidates(direct)
        sorted_candidates = sorted(
            expanded,
            key=lambda item: (-self._score_candidate(item, direct), item)
        )
        return sorted_candidates

    def resolve_dc_name(self, value):
        direct = {_val for val in _iter_values(value) if (_val := self._normalize_dc(val))}
        return self._pick_best(direct)
