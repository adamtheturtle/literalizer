module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    // outer heading
    // first empty
    ("a", FMap []);
    // second empty
    ("b", FMap [])
]
