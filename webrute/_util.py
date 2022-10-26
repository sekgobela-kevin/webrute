import inspect


def has_implicit_argument(_callable):
    # Checks if callable has implicit argument(checks 'cls' and 'self')
    arguments = list(inspect.signature(_callable).parameters)
    return bool(arguments) and arguments[0] in ["self", "cls"]

def extract_arguments(_callable, skip_implicit=False):
    # Extracts arguments from callable
    arguments = list(inspect.signature(_callable).parameters)
    if skip_implicit and arguments:
        # Skips self and cls arguments as they are implicit.
        # Dont use 'self' or 'cls' for non implicit arguments.
        if arguments and arguments[0] in ["self", "cls"]:
            arguments = arguments[1:]
    return arguments