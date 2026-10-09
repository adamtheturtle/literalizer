module Main

type Val =
    | FStr of string
    | FList of Val list
let consume (_value: obj) : obj = null
let item: Val = FStr "s"
consume(item)
