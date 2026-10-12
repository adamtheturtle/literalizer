module Main

type Val =
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FList [
    FMap [("nested", FMap [("times", FList [FStr "1900-01-01T00:00:00+00:00"])])];
    FMap []
]
