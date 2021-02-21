# just comment line
COMMENT_REGEX = "\s*(//.*$)?$"

# everything that's redundant in a line- comments, white-spaces, etc.
REDUNDANT_PARTS = "^\s*(?P<command>[\w\s.-]*)(?://.*)?$"
