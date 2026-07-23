module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
let process (_data: obj) : obj = null
process(FList [FInt 1L; FStr "x"])
