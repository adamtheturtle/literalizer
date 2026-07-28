module Main

type Val =
    | FInt of int64
    | FList of Val list
let process (_data: obj) : obj = null
let unknown_value: Val = FList [
    FInt 1L
]
process(unknown_value)
