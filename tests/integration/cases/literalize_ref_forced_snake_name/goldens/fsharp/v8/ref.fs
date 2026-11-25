module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let user_obj: Val = FMap [
    ("_", FStr "_")
]
let my_data: Val = user_obj
