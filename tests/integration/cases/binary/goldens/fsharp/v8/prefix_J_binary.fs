module Main

type Val =
    | JStr of string
    | JList of Val list
let my_data: Val = JList [
    JStr "48656c6c6f"
]
