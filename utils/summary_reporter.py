# utils/summary_reporter.py

# ANSI escape codes for colors
COLOR_RED = '\033[91m'
COLOR_GREEN = '\033[92m'
COLOR_YELLOW = '\033[93m'
COLOR_BLUE = '\033[94m'
COLOR_RESET = '\033[0m'

def generate_summary(conversion_results, skipped_entities, failed_conversions):
    """
    Generates and prints a detailed analytical summary of the conversion process.
    """
    print(f"\n{COLOR_BLUE}--- Analytical Summary ---{COLOR_RESET}")

    # --- Overall Summary Table ---
    print(f"\n{COLOR_BLUE}Overall Conversion Status:{COLOR_RESET}")
    print(f"{'Source/Target Entity Type':<80} {'Source Count':<15} {'Converted Count':<18} {'Status':<10}")
    print(f"{'-'*80:<80} {'-'*15:<15} {'-'*18:<18} {'-'*10:<10}")

    detailed_discrepancies = []

    # Define entities that are known to be derived from others, not from a direct source file
    DERIVED_ENTITIES = ['cluster_virtualization', 'dc_az', 'dc_region']

    # Sort results to have a consistent order
    sorted_results = sorted(conversion_results, key=lambda x: x.get('source_name') or '')

    for result in sorted_results:
        source_name = result.get('source_name', 'Unknown')
        source_count = result.get('source_count', 0)
        target_counts = result.get('target_counts', {})
        status = result.get('status', 'UNKNOWN')

        total_converted = sum(target_counts.values())

        status_color = COLOR_RESET
        status_text = ""

        # Determine status based on counts
        is_match = False
        if status == 'SUCCESS':
            if not target_counts: # Source entities exist but nothing was converted
                if source_count > 0:
                    is_match = False
                else: # source_count is 0 and no targets, so it's fine
                    is_match = True
            elif len(target_counts) == 1:
                # For simple 1-to-1 or 1-to-N conversions, counts must match exactly.
                is_match = (source_count == total_converted)
            else: # len(target_counts) > 1
                # For complex 1-to-many conversions (like vaults), assume a match 
                # if the source count matches ANY of the primary target counts.
                # This is a heuristic based on user feedback.
                is_match = source_count in target_counts.values()

        is_derived = source_name in DERIVED_ENTITIES and source_count == 0 and total_converted > 0

        if status == 'FAILED':
            status_color = COLOR_RED
            status_text = "FAILED"
            if source_count > 0:
                 detailed_discrepancies.append(f"  - Source entity '{source_name}' ({source_count} found) failed to convert.")
        elif is_derived:
            status_color = COLOR_YELLOW
            status_text = "DERIVED"
        elif is_match:
            status_color = COLOR_GREEN
            status_text = "OK"
        else:
            status_color = COLOR_RED
            status_text = "MISMATCH"
            detailed_discrepancies.append(f"  - Source '{source_name}' ({source_count} found) resulted in {total_converted} converted entities.")

        # Override status for N/A cases
        if source_count == 0 and total_converted == 0 and status != 'FAILED':
            status_text = "N/A"
            status_color = COLOR_YELLOW
        
        # Print the main source entity line
        print(f"{source_name:<80} {source_count:<15} {total_converted:<18} {status_color}{status_text:<10}{COLOR_RESET}")

        # Print the target entities indented
        for target_name, target_count in sorted(target_counts.items()):
            print(f"{'  -> ' + target_name:<80} {'':<15} {target_count:<18} {'':<10}")

    # --- Skipped and Failed Conversions ---
    if skipped_entities or failed_conversions:
        print(f"\n{COLOR_BLUE}Issues During Conversion:{COLOR_RESET}")
        if skipped_entities:
            print(f"\n{COLOR_YELLOW}  Skipped Entities (no converter found):{COLOR_RESET}")
            for entity in skipped_entities:
                print(f"    - {entity}")
        if failed_conversions:
            print(f"\n{COLOR_RED}  Failed Conversions:{COLOR_RESET}")
            for failure in failed_conversions:
                print(f"    - Entity: {failure['entity']}, Reason: {failure['reason']}")

    # --- Detailed Discrepancies ---
    if detailed_discrepancies:
        print(f"\n{COLOR_BLUE}Detailed Discrepancies:{COLOR_RESET}")
        for discrepancy in detailed_discrepancies:
            print(discrepancy)
    
    print(f"\n{COLOR_BLUE}--- End of Summary ---{COLOR_RESET}")
