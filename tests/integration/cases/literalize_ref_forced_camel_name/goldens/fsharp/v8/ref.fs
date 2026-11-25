module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let userObj: Val = FMap [
    ("_", FStr "_")
]
let my_data: Val = userObj
