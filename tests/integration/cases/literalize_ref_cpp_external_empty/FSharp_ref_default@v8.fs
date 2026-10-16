module Main

type Val =
    | FInt of int64
    | FList of Val list
let item: Val = FList [
    FInt 1L;
    FInt 2L
]
let my_data: Val = FList [
    FInt 1L;
    FInt 2L
]
(void)my_data;
let my_data: Val = item
(void)my_data;
