module Main

type Val =
    | JFloat of float
    | JList of Val list
let my_data: Val = JList [
    JFloat 1.0e-09;
    JFloat(-1.0e-09)
]
