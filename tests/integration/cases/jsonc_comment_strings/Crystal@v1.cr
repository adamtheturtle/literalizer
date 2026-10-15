module Fixture_jsonc_comment_strings_Crystal
extend self
my_data = [
    # strings stay data
    "https://example.org/a/*b*/",  # URL annotation
    "escaped quote: \" // still data",
    "backslash: \\",  # outside the string
    "/* not a comment */",
]
end
