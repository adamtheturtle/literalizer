module Main

let record (_value: obj) : obj = null
let flush (_count: obj) : obj = null
type Val =
    | FInt of int64
    | FList of Val list
record(42)
flush(3)
