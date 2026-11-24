module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let mutable my_data: Val = FMap []
