module Main

type Val =
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FList [
    FMap [("timestamp", FStr "2040-01-01T03:00:00+03:00")];
    FMap []
]
