module Main

type Val =
    | FInt of int64
    | FList of Val list
let process (_a: obj, _b: obj, _c: obj, _d: obj) : obj = null
process(1, 2, 3, 4)
process(10, 20, 30, 40)
