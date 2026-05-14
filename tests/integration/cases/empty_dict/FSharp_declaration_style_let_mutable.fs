module Main

type Val =
    | FMap of (string * Val) list
let mutable my_data: Val = FMap []
