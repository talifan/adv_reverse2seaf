_ID_PREFIX = 'tenant'


def set_prefix(prefix: str | None):
    """Forcefully set global prefix used for generated identifiers."""
    global _ID_PREFIX
    if prefix and isinstance(prefix, str) and prefix.strip():
        _ID_PREFIX = prefix.strip()


def get_prefix() -> str:
    """Return current identifier prefix."""
    return _ID_PREFIX


def build_id(*parts: str) -> str:
    """Construct an identifier by concatenating current prefix and parts with dots."""
    cleaned = [str(part).strip() for part in parts if part]
    return '.'.join([_ID_PREFIX, *cleaned]) if cleaned else _ID_PREFIX


def _infer_prefix_from_source(source_data) -> str | None:
    if not isinstance(source_data, dict):
        return None
    for entity in source_data.values():
        if isinstance(entity, dict):
            for key in entity.keys():
                if isinstance(key, str) and '.' in key:
                    candidate = key.split('.', 1)[0].strip()
                    if candidate and candidate.lower() not in {'seaf', 'metadata'}:
                        return candidate
    return None


def ensure_prefix(prefix: str | None = None, source_data=None) -> str:
    """Ensure prefix is set. Override takes precedence; otherwise infer from source data."""
    global _ID_PREFIX
    if prefix and isinstance(prefix, str) and prefix.strip():
        _ID_PREFIX = prefix.strip()
        return _ID_PREFIX
    if _ID_PREFIX != 'tenant' or source_data is None:
        return _ID_PREFIX
    inferred = _infer_prefix_from_source(source_data)
    if inferred:
        _ID_PREFIX = inferred
    return _ID_PREFIX


def dc_ref(name: str) -> str:
    return build_id('dc', name)


def dc_az_ref(name: str) -> str:
    return build_id('dc_az', name)


def vpc_ref(vpc: str) -> str:
    return build_id('vpcs', vpc)


def subnet_ref(subnet: str) -> str:
    return build_id('subnets', subnet)


def kb_ref(tag: str, auth_type: str) -> str:
    return build_id('kb', tag.lower(), auth_type.lower())

def segment_ref(dc_name: str, segment_name: str) -> str:
    return build_id('segment', dc_name, segment_name)

def get_name_from_ref(ref: str) -> str | None:
    """Extracts the name part from a reference string (e.g., 'prefix.dc.my-dc' -> 'my-dc')."""
    if not ref or not isinstance(ref, str) or '.' not in ref:
        return None
    return ref.split('.')[-1]
