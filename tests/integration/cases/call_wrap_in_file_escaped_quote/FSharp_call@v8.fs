module Main

let process (_v: obj) : obj = null
type Val =
    | FStr of string
    | FList of Val list
process("a\"b")
