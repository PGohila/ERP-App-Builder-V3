import re

def remove_special_characters(input_string):
    # Define a regular expression pattern to match special characters
    pattern = r'[^a-zA-Z0-9\s]+'  # Match special characters except spaces

    # Use the sub() function to replace special characters with an empty string
    cleaned_string = re.sub(pattern, '', input_string)

    # Replace consecutive spaces with a single underscore
    cleaned_string = re.sub(r'\s+', '_', cleaned_string)

    # Trim underscores at the beginning and end of the string
    cleaned_string = cleaned_string.strip('_')

    return cleaned_string

# Example usage
input_string = "!! Hello @World$%"
cleaned_string = remove_special_characters(input_string)
print(cleaned_string)  # Output: 'Hello_World'
