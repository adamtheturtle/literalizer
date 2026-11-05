module Main

type Val =
    | FNull
    | FBool of bool
    | FFloat of float
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("b", FNull);
    ("a", FMap [("y", FList [FFloat 1.0]); ("x", FBool false)])
]
