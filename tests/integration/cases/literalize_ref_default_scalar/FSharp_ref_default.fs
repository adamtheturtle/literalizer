module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let my_var: Val = FInt 1L
let my_data: Val = my_var
