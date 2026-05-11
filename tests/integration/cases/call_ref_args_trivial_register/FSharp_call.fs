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
process(my_int, 42)
process(my_bool, 7)
process(my_float, 9)
process(my_list, 1)
