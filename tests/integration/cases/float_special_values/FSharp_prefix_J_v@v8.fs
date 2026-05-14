module Main

type Val =
    | JFloat of float
    | JList of Val list
let my_data: Val = JList [
    JFloat infinity;
    JFloat(-infinity);
    JFloat nan
]
