module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    // heading
    ("a", FStr "single ' // data");
    ("b", FStr "linecontinuation");
    ("c", FStr "\\");  // actual comment
    ("d", FStr "  ")  // final comment
]
