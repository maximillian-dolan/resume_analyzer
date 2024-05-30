import re

def extract_section(text, section_title):
    pattern = rf'{section_title}.*?(?=(\\n[A-Z]|$))'
    match = re.search(pattern, text, re.DOTALL)
    return match.group(0) if match else ''

def format_entry(entries, section_title):
    formatted_entries = []
    for entry in entries:
        lines = entry.strip().split('\n')
        if len(lines) < 4:
            continue
        place = lines[0].strip()
        location = lines[1].strip()
        role_date = lines[2].strip().split('‑')
        role = role_date[0].strip()
        date = role_date[-1].strip()
        infos = [f'info: {line.strip()}' for line in lines[3:]]
        formatted_entries.append(
            f'place: {place}\nlocation: {location}\nrole: {role}\ndate: {date}\n' + '\n'.join(infos)
        )
    return f'{section_title}\n\n' + '\n\n'.join(formatted_entries)

with open('resume.txt', 'r') as file:
    text = file.read()

# Extract sections
education_text = extract_section(text, 'Education')
skills_text = extract_section(text, 'Skills')
experience_text = extract_section(text, 'Work Experience')

# Process and format education and experience entries
education_entries = education_text.split('\n\n')[1:]  # Skip the section title
experience_entries = experience_text.split('\n\n')[1:]  # Skip the section title

formatted_education = format_entry(education_entries, 'Education')
formatted_experience = format_entry(experience_entries, 'Work Experience')

# Write to separate files
with open('education.txt', 'w') as file:
    file.write(formatted_education)

with open('skills.txt', 'w') as file:
    file.write(skills_text)

with open('experience.txt', 'w') as file:
    file.write(formatted_experience)
