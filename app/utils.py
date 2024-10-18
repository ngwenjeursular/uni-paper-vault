import re
from flask import url_for
from app.models import User  # Import your User model

def parse_tags(content):
    """
    Function to parse user tags in comments and convert them to profile links.
    """
    tag_pattern = r'@(\w+)'  # Assuming usernames are alphanumeric

    def replace_tag(match):
        username = match.group(1)
        # Query user by username
        user = User.query.filter_by(username=username).first()

        if user:
            # Return the link to the user's profile
            return f'<a href="{url_for("user.profile", user_id=user.id)}">@{username}</a>'
        else:
            return f'@{username}'  # Return plain text if user not found

    return re.sub(tag_pattern, replace_tag, content)
