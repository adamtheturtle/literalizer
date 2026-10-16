module Main

type Val =
    | FInt of int64
    | FList of Val list
let ref_data: Val = FList [
    FInt 1L;
    FInt 2L
]
let my_data: Val = FList [
    FInt 0L
]
(void)my_data;
let my_data: Val = ref_data
(void)my_data;
