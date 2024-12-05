from flask_bleach import Bleach

# Initialize Flask-Bleach
bleach = Bleach()

def sanitize_form_data(form_data, allowed_tags=None, allowed_attributes=None):
    """
    Sanitizes all fields in a form's data to prevent XSS and other vulnerabilities.

    Args:
        form_data (dict): The form data as a dictionary.
        allowed_tags (list, optional): Tags allowed in the input (default: None).
        allowed_attributes (dict, optional): Attributes allowed in the input (default: None).

    Returns:
        dict: The sanitized form data.

    Example:
        >>> form_data = {
        ...     "name": "<b>John</b> <script>alert('XSS')</script>",
        ...     "description": "<a href='https://example.com'>Click Here</a>"
        ... }
        >>> allowed_tags = ['b', 'a']
        >>> allowed_attributes = {'a': ['href']}
        >>> sanitize_form_data(form_data, allowed_tags, allowed_attributes)
        {
            "name": "<b>John</b> ",
            "description": "<a href='https://example.com'>Click Here</a>"
        }
    """
    sanitized_data = {}
    for field, value in form_data.items():
        if isinstance(value, str):
            sanitized_data[field] = bleach.clean(
                value,
                tags=allowed_tags or bleach.ALLOWED_TAGS,
                attributes=allowed_attributes or bleach.ALLOWED_ATTRIBUTES
            )
        else:
            sanitized_data[field] = value  # Non-string data is left unchanged
    return sanitized_data
