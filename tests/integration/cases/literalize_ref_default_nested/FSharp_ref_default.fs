module Main

type Val =
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let item_var: Val = FMap [
    ("_", FStr "_")
]
let my_data: Val = FMap [
    ("items", FList [item_var; FMap [("fallback", FStr "value")]])
]
