module Main

type Val =
    | FInt of int64
    | FList of Val list
    | FStr of string
    | FDatetime of System.DateTime
let process (_value: obj) : obj = null
process(FStr (string (System.TimeOnly(9, 30, 0))))
process(FStr (string (System.DateTime(2024, 1, 15, 0, 0, 0))))
process(FInt 1L)
