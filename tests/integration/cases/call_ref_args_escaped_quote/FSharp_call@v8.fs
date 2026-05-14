module Main

type Val =
    | FStr of string
    | FList of Val list
let process (_v: obj) : obj = null
let my_str: Val = FStr "a\"b"
process(my_str)
