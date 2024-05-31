import re

def extract_section(text, section_title):
    pattern = rf'{section_title}.*?(?=(\\n[A-Z]|$))'
    match = re.search(pattern, text, re.DOTALL)
    return match.group(0) if match else ''

def format_entry(entries, section_title):
    formatted_entries = []
    for entry in entries:
        if len(entry) < 4:
            continue
        place = entry[0].strip().split('  ')[0].strip()
        location = entry[0].strip().split('  ')[-1].strip()
        role = entry[1].strip().split('  ')[0].strip()
        date = entry[1].strip().split('  ')[-1].strip()
        infos = [f'info: {line.replace("*","").strip()}' for line in entry[2:]]
        formatted_entries.append(
            f'place: {place}\nlocation: {location}\nrole: {role}\ndate: {date}\n' + '\n'.join(infos)+'\n'
        )
    return '\n'.join(formatted_entries)

def remove_specific_hyphens(s):
    return re.sub(r'(?<!\s)‑(?!\s)', '', s)

def split_by_empty_strings(strings):
    
    result = []
    current_sublist = []
    for s in strings:
        if s == '':
            # If an empty string is encountered and the current sublist is not empty           
            result.append(current_sublist)
            # Reset the current sublist
            current_sublist = []
        else:
            # If the string is not empty, add it to the current sublist
            current_sublist.append(s)
    result.append(current_sublist)
    
    return result


with open('resume.txt', 'r') as file:
    text = file.read()

text = text.replace('References available upon request.', '')

# Define sections
sections = ['Education','Skills','Projects','Work Experience']
sections_texts = {}

# Find the start and end indices for each section
for i, section in enumerate(sections):
    start_index = text.find(section)
    end_index = text.find(sections[i + 1]) if i + 1 < len(sections) else len(text)
    section_text = text[start_index:end_index].strip()
    
    # Split the section text into lines
    lines = section_text.split('\n')
    
    # Remove the first line, and lines that contain only a single number
    cleaned_lines = [line for line in lines[1:] if not re.match(r'^\d+$', line.strip())]
    
    # Removes blank lines at start and end
    while cleaned_lines[0].strip == '':
        cleaned_lines = cleaned_lines[1:]
    while cleaned_lines[-1].strip() == '':
        cleaned_lines = cleaned_lines[:-1]

    # Join the cleaned lines back into a single string
    cleaned_section_text = '\n'.join(cleaned_lines)
    
    # MAYBE DONT JOIN AGAIN AND INSTEAD LEAVE AS LIST OF LINES; SEPERATE BY BLANK STRINGS

    sections_texts[section] = cleaned_lines
    #print('===========================')
    #print(f'{section}:\n{cleaned_section_text}\n')
    #print('=============================')


# Display the result
formatted_sections = {}
for section, content in sections_texts.items():
    
    # Format strings nicely
    modified_content = []
    for i, string in enumerate(content):
        string = string.replace('•','*')

        #Remove \x0c and replace with space (happens when moving to second page)
        if string.startswith('\x0c'):
            modified_content.append('')  # Add an empty string
            modified_content.append(string[1:])  # Add the string without the '\x0c' part
        else:
            modified_content.append(string)  # Add the string as it is
        
        if i >3:
            if ('*' not in string) and ('*' in modified_content[-2]) and string != '':

                # Join bullet points back together
                modified_content[-2] = modified_content[-2].strip() + modified_content[-1].strip()
                modified_content = modified_content[:-1]

    # Remove hyphens inbetween words
    content = [remove_specific_hyphens(s) for s in modified_content]

    entries = split_by_empty_strings(content)

    # Leave skills as is
    if section != 'Skills':
        formatted_section = format_entry(entries, section)
    elif section == 'Skills':
        formatted_section = '\n'.join(entries[0])

    formatted_sections[section] = formatted_section

# Change 'Work Experience' to 'Experience'
formatted_sections['Experience'] = formatted_sections['Work Experience']
del formatted_sections['Work Experience']

# Save each section
for section, content in formatted_sections.items():
    with open(f'{section}.txt','w') as file:
        file.write(content)
