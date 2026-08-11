module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
let process (_data: obj, _count: obj) : obj = null
let my_ints: Val = FList [
    FInt 1L;
    FInt 2L;
    FInt 3L
]
let my_strings: Val = FList [
    FStr "a";
    FStr "b"
]
let my_empty: Val = FList []
process(my_ints, FInt 42L)
process(my_strings, FInt 7L)
process(my_empty, FInt 99L)
