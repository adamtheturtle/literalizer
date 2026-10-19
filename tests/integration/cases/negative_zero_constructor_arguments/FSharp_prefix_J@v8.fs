module Main

type Val =
    | JFloat of float
    | JList of Val list
let my_data: Val = JList [
    JFloat(-0.0);
    JFloat 0.0
]
