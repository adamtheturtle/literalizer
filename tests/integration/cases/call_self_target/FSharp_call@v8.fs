module Main

type Val =
    | FStr of string
    | FList of Val list
let self (_value: obj) : obj = null
self(FStr "hello")
