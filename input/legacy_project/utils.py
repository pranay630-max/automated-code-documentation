def validate_email(email):

    if "@" not in email:
        return False

    if "." not in email:
        return False

    return True


def format_name(first_name, last_name):

    return (
        first_name.strip().title()
        + " "
        + last_name.strip().title()
    )