module Main

type Val =
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FList [
    FMap [("first", FStr "Alice"); ("last", FStr "Smith")];
    FMap [("first", FStr "Bob"); ("middle", FStr "Quincy")]
]
