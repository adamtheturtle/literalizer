module Main

let do_thing (_x_: obj) : obj = null
type Val =
    | FInt of int64
    | FList of Val list
do_thing(FInt 1L)
do_thing(FInt 2L)
