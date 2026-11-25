module Fixture_string_with_backslash_Crystal_type_hints_safe
extend self
my_data = [
    "C:\\path\\to\\file",
    "back\\\\slash",
    "hello \\\"world\\\"",
    "path\\to \"# file",
    "trailing\\",
    "both \"quotes''' here",
    "line1\\nline2\nwith newline",
]
end
