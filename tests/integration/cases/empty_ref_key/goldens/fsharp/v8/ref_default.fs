module Main

type Val =
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let external_value: Val = FMap [
    ("_", FStr "_")
]
let my_data: Val = FList [
    external_value
]
