module Main

type Val =
    | FInt of int64
    | FList of Val list
let process (_data: obj) : obj = null
let known_value: Val = FInt 1L
let unknown_value: Val = FList []
process(unknown_value)
