module Main

type Val =
    | FStr of string
    | FList of Val list
let my_data: Val = FList [
    FStr "C:\\path\\to\\file";
    FStr "back\\\\slash";
    FStr "hello \\\"world\\\"";
    FStr "path\\to \"# file";
    FStr "trailing\\";
    FStr "both \"quotes''' here";
    FStr "line1\\nline2\nwith newline"
]
