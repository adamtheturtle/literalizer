module Main

type Val =
    | FStr of string
    | FList of Val list
let op (_value: obj) : obj = null
op("hello")
