module Main

type Val =
    | FInt of int64
    | FList of Val list
    | FStr of string
    | FDatetime of System.DateTime
let process (_value: obj) : obj = null
process(System.TimeOnly(9, 30, 0))
process(System.DateTime(2024, 1, 15, 0, 0, 0))
process(1)
