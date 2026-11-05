module Main

type Val =
    | FBool of bool
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("keep", FBool true);
    ("skip", FBool false)
]
