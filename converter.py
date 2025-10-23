# main converter script

# Note: This script requires the PyYAML library.
# You can install it using: pip install PyYAML

import argparse
import yaml
import os
from pathlib import Path
import sys

# Add utils and modules to the python path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_dir, 'utils'))
sys.path.append(os.path.join(script_dir, 'modules'))

from file_io import load_source_data, save_converted_data
from summary_reporter import generate_summary
from id_prefix import ensure_prefix

# Explicitly import converter modules
from dc_region_converter import convert as dc_region_convert
from dc_az_converter import convert as dc_az_convert
from dc_converter import convert as dc_convert # Added DC converter
from vpcs_converter import convert as vpcs_convert
from subnets_converter import convert as subnets_convert
from ecss_converter import convert as ecss_convert
from cluster_virtualization_converter import convert as cluster_virtualization_convert
from cces_converter import convert as cces_convert
from rdss_converter import convert as rdss_convert
from nat_gateways_converter import convert as nat_gateways_convert
from peerings_converter import convert as peerings_convert
from vaults_converter import convert as vaults_convert
from vpn_gateways_converter import convert as vpn_gateways_convert
from vpn_connections_converter import convert as vpn_connections_convert
from eips_converter import convert as eips_convert
from dmss_converter import convert as dmss_convert
from security_groups_converter import convert as security_groups_convert
from branches_converter import convert as branches_convert
from elbs_converter import convert as elbs_convert # Added ELB converter

# Map entity names to their converter functions
CONVERTERS = {
    'dc_region': dc_region_convert,
    'dc_az': dc_az_convert,
    'dcs': dc_convert, # Added DC converter
    'vpcs': vpcs_convert,
    'subnets': subnets_convert,
    'ecss': ecss_convert,
    'cluster_virtualization': cluster_virtualization_convert,
    'cces': cces_convert,
    'rdss': rdss_convert,
    'nat_gateways': nat_gateways_convert,
    'peerings': peerings_convert,
    'vaults': vaults_convert,
    'vpn_gateways': vpn_gateways_convert,
    'vpn_connections': vpn_connections_convert,
    'eips': eips_convert,
    'dmss': dmss_convert,
    'security_groups': security_groups_convert,
    'branches': branches_convert,
    'elbs': elbs_convert, # Added ELB converter
}

def load_config(config_path):
    """Loads configuration from a YAML file."""
    if not os.path.exists(config_path):
        print(f"Warning: Config file not found at {config_path}. Using defaults.")
        return {}
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def determine_prefix(source_data, override):
    return ensure_prefix(prefix=override, source_data=source_data)


def main():
    """Main function to run the conversion process."""

    # 1. Argument Parsing
    parser = argparse.ArgumentParser(description='Convert cloud architecture data to SEAF-core format.')
    parser.add_argument('--input-dir', type=str, help='Input directory with source files.')
    parser.add_argument('--output-dir', type=str, help='Output directory for converted files.')
    parser.add_argument('--id-prefix', type=str, help='Identifier prefix to use for generated entity IDs (overrides config and auto detection).')
    parser.add_argument('--config', type=str, default='converter_config.yaml', help='Path to the configuration file.')
    parser.add_argument('entities', nargs='*', help='Specific entities to convert (e.g., vpcs subnets). Overrides config file.')

    args = parser.parse_args()

    # 2. Load Configuration
    config_path = Path(script_dir) / args.config  # Resolve config path relative to script_dir
    config = load_config(config_path)

    # 3. Merge CLI arguments with config file (CLI overrides config)
    base_dir = Path.cwd()
    input_dir = Path(args.input_dir or config.get('input_dir') or base_dir)
    output_dir = Path(args.output_dir or config.get('output_dir') or base_dir)
    id_prefix_override = args.id_prefix or config.get('id_prefix')
    
    # CLI entities list overrides config if provided
    if args.entities:
        entities_to_convert = args.entities
    else:
        entities_to_convert = config.get('entities_to_convert', ['__all__'])

    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    print("--- Conversion Started ---\n")
    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}")
    print(f"Entities to convert: {', '.join(entities_to_convert)}")
    print("--------------------------")

    # 4. Load source data
    print("\nLoading source files...")
    source_data = load_source_data(input_dir)
    determine_prefix(source_data, id_prefix_override)
    if not source_data:
        print("[ERROR] No source data loaded. Aborting.")
        return
    print("Source files loaded.")

    # --- Analytical Summary Tracking ---
    conversion_results = []
    skipped_entities = []
    failed_conversions = []
    converted_files = []

    if '__all__' in entities_to_convert:
        entities_to_convert = list(CONVERTERS.keys())

    # Create a mapping from short entity name to full source name
    source_name_map = {}
    for key in source_data.keys():
        short_name = key.split('.')[-1]
        source_name_map[short_name] = key

    # 5. Call converters
    print("\nStarting entity conversion...")
    for entity_name in entities_to_convert:
        if entity_name in CONVERTERS:
            source_full_name = source_name_map.get(entity_name)
            try:
                print(f"  - Converting {entity_name}...")
                convert_function = CONVERTERS[entity_name]
                converted_data = convert_function(source_data)

                # Determine source count
                source_count = 0
                if source_full_name and source_full_name in source_data and isinstance(source_data[source_full_name], dict):
                    source_count = len(source_data[source_full_name])

                # Process and save converted data, and collect target counts
                target_counts = {}
                if converted_data and isinstance(converted_data, dict):
                    for target_full_name, entities in converted_data.items():
                        count = len(entities) if isinstance(entities, dict) else 0
                        target_counts[target_full_name] = count
                        
                        # Save each target entity to its own file
                        # Determine the file name based on the target entity type
                        if target_full_name == 'seaf.ta.components.network':
                            base_file_name = 'network_devices'
                        elif target_full_name == 'seaf.ta.services.network':
                            base_file_name = 'networks'
                        else:
                            # Default to the last part of the entity name for other types
                            base_file_name = target_full_name.split('.')[-1]
                        
                        file_name = f"{base_file_name}.yaml"
                        save_converted_data(output_dir, base_file_name, {target_full_name: entities})
                        converted_files.append(file_name)
                
                # Store results for summary
                conversion_results.append({
                    'source_name': source_full_name or entity_name,
                    'source_count': source_count,
                    'target_counts': target_counts,
                    'status': 'SUCCESS'
                })

            except Exception as e:
                print(f"    [ERROR] Failed to convert {entity_name}: {e}")
                failed_conversions.append({'entity': entity_name, 'reason': str(e)})
                # Find source count even if conversion fails
                source_count = 0
                if source_full_name and source_full_name in source_data and isinstance(source_data[source_full_name], dict):
                    source_count = len(source_data[source_full_name])
                conversion_results.append({
                    'source_name': source_full_name or entity_name,
                    'source_count': source_count,
                    'target_counts': {},
                    'status': 'FAILED'
                })
        else:
            print(f"    [WARNING] No converter found for entity '{entity_name}'. Skipping.")
            skipped_entities.append(entity_name)

    # 6. Generate root.yaml
    if converted_files:
        print("\nGenerating root.yaml...")
        root_yaml_content = {'imports': sorted(list(set(converted_files)))} # Use set to remove duplicates and sort
        root_yaml_path = os.path.join(output_dir, 'root.yaml')
        with open(root_yaml_path, 'w') as f:
            yaml.dump(root_yaml_content, f, allow_unicode=True, sort_keys=False)
        print(f"  [SUCCESS] Generated root.yaml at {root_yaml_path}")
    else:
        print("\nNo files converted, skipping root.yaml generation.")

    print("\n--- Conversion Finished ---\n")

    # --- Analytical Summary ---
    generate_summary(conversion_results, skipped_entities, failed_conversions)


if __name__ == '__main__':
    main()
