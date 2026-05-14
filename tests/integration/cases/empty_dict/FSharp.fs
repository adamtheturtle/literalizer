module Main

type Val =
    | FMap of (string * Val) list
let my_data: Val = FMap []
