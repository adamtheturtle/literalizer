module Main

type Val =
    | FStr of string
let mutable my_data: Val = FStr "hello"
