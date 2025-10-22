# utils/warning_reporter.py

def report_warning(entity_id, field_name, message):
    """
    Reports a warning about a missing or invalid field during conversion.
    """
    print(f"WARNING: Entity '{entity_id}' - Field '{field_name}': {message}")

# Optionally, collect warnings for a summary report
_warnings = []

def collect_warning(entity_id, field_name, message):
    _warnings.append(f"WARNING: Entity '{entity_id}' - Field '{field_name}': {message}")

def get_collected_warnings():
    return _warnings

def clear_collected_warnings():
    _warnings.clear()
