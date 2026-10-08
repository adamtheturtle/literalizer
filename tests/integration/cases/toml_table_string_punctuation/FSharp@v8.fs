module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("comma_hash", FStr "a,#b");
    ("comma_space_hash", FStr "trail, # comment");
    ("escaped_quote", FStr "quote \" and , #");
    ("next_line", FStr "xy");
    ("line_separator", FStr "x y");
    ("paragraph_separator", FStr "x y")
]
