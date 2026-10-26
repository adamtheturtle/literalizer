datatype val_t =
    SStr of string
  | SList of val_t list
val my_data : val_t = SList [
    SStr "C:\\path\\to\\file",
    SStr "back\\\\slash",
    SStr "hello \\\"world\\\"",
    SStr "path\\to \"# file",
    SStr "trailing\\",
    SStr "both \"quotes''' here",
    SStr "line1\\nline2\nwith newline"
]
val _ = my_data
