module Main

type Val =
    | JFloat of float
    | JList of Val list
let my_data: Val = JList [
    JFloat 1.1;
    JFloat(-2.2);
    JFloat 3.3
]
