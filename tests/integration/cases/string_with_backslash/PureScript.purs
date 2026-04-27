module Check where


data Val
    = PStr String
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PStr "C:\\path\\to\\file",
    PStr "back\\\\slash",
    PStr "hello \\\"world\\\"",
    PStr "path\\to \"# file",
    PStr "trailing\\",
    PStr "both \"quotes''' here",
    PStr "line1\\nline2\nwith newline"
    ]
