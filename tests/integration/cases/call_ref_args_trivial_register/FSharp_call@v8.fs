module Main

type Val =
    | FBool of bool
    | FInt of int64
    | FFloat of float
    | FList of Val list
let process (_value: obj, _count: obj) : obj = null
let my_int: Val = FInt 1L
let my_bool: Val = FBool true
let my_float: Val = FFloat 3.14
let my_list: Val = FList [
    FInt 1L;
    FInt 2L;
    FInt 3L
]
process(my_int, FInt 42L)
process(my_bool, FInt 7L)
process(my_float, FInt 9L)
process(my_list, FInt 1L)
