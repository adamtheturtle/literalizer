(use-modules (json))
(define my_data (vector
    "C:\\path\\to\\file"
    "back\\\\slash"
    "hello \\\"world\\\""
    "path\\to \"# file"
    "trailing\\"
    "both \"quotes''' here"
    "line1\\nline2\nwith newline"
))
