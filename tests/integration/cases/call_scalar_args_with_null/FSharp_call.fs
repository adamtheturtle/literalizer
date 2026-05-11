module Main

type Val =
    | FNull
    | FStr of string
    | FList of Val list
let process (_value: obj) : obj = null
process(FNull)
process("hello")
