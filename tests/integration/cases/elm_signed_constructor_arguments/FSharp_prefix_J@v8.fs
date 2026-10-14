module Main

type Val =
    | JInt of int64
    | JFloat of float
    | JList of Val list
let my_data: Val = JList [
    JInt(-42L);
    JInt 0L;
    JInt 42L;
    JFloat(-1.25);
    JFloat 0.0;
    JFloat 1.25
]
