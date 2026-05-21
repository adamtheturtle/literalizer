module Main

let process (_a: obj, _b: obj) : obj = null
type Val =
    | FInt of int64
    | FList of Val list
process(1, 2)
