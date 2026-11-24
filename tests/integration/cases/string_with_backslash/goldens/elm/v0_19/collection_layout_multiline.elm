module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)


my_data : Val
my_data = EList [
    EStr "C:\\path\\to\\file",
    EStr "back\\\\slash",
    EStr "hello \\\"world\\\"",
    EStr "path\\to \"# file",
    EStr "trailing\\",
    EStr "both \"quotes''' here",
    EStr "line1\\nline2\nwith newline"
    ]
