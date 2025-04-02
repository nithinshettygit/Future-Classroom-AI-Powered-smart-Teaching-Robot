import json

def integrate_figures(schedule_file, output_file, integrated_file):
    # Load the JSON files
    with open(schedule_file, 'r', encoding='utf-8') as f:
        schedule_data = json.load(f)
    
    with open(output_file, 'r', encoding='utf-8') as f:
        output_data = json.load(f)
    
    # Create a dictionary for quick lookup of figures by chapter and subchapter
    figures_lookup = {}
    for item in output_data:
        key = (item['chapter'], item['subchapter'])
        figures_lookup[key] = item.get('figures', [])
    
    # Integrate figures into schedule data
    for day in schedule_data:
        for topic in day['topics']:
            key = (topic['chapter'], topic['subchapter'])
            topic['figures'] = figures_lookup.get(key, [])
    
    # Save the integrated data
    with open(integrated_file, 'w', encoding='utf-8') as f:
        json.dump(schedule_data, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully created {integrated_file}")

# File paths
schedule_file = 'schedule.json'
output_file = 'output.json'
integrated_file = 'integrated.json'

# Run the integration
integrate_figures(schedule_file, output_file, integrated_file)