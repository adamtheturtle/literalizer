module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("double", FStr "a b");
    ("single", FStr "c d");
    // A comment, which both separators would end.
    ("both", FStr "e f g");
    ("continued", FStr "hi");
    ("escaped backslash", FStr "j\\ k")
]
