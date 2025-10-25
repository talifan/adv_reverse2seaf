import os
import yaml
from pathlib import Path

def load_source_data(input_dir):
    """
    Loads all YAML files from a directory and merges them into a single dictionary.
    It assumes each YAML file has a single top-level key representing the entity type.
    """
    if not os.path.isdir(input_dir):
        print(f"[ERROR] Input directory not found: {input_dir}")
        return {}

    aggregated_data = {}
    for filename in os.listdir(input_dir):
        if filename.endswith('.yaml') or filename.endswith('.yml'):
            file_path = os.path.join(input_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    data = yaml.safe_load(f)
                    if data:
                        aggregated_data.update(data)
                except yaml.YAMLError as e:
                    print(f"Error parsing YAML file {filename}: {e}")
    return aggregated_data

def save_converted_data(output_dir, entity_name, data, merge=True):
    """
    Saves the converted data to a YAML file in the specified output directory.
    If the file already exists, it merges the new data with the existing data.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    file_path = os.path.join(output_dir, f"{entity_name}.yaml")
    
    existing_data = {}
    if merge and os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                existing_data = yaml.safe_load(f)
                if not existing_data: # Handle empty file case
                    existing_data = {}
            except yaml.YAMLError as e:
                print(f"Warning: Error parsing existing YAML file {file_path}: {e}. Overwriting.")
                existing_data = {}
    
    # Merge new data with existing data
    # Assuming 'data' is a dictionary with a single top-level key (e.g., 'seaf.ta.components.network')
    # and its value is a dictionary of entities.
    for top_level_key, entities in data.items():
        if top_level_key not in existing_data:
            existing_data[top_level_key] = {}
        existing_data[top_level_key].update(entities)

    # Dump the merged data to a string and perform placeholder replacement for comments
    yaml_string = yaml.dump(existing_data, allow_unicode=True, sort_keys=False)

    # This is a workaround to add comments, as PyYAML does not support it natively.
    final_yaml_string = yaml_string.replace(
        "'###PLACEHOLDER_FOR_MANUAL_ZONE###'",
        " ### <--- Заполнить вручную"
    )

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(final_yaml_string)
    action = "Saved/Merged" if merge else "Saved"
    print(f"    [SUCCESS] {action} converted {entity_name} to {file_path}")
