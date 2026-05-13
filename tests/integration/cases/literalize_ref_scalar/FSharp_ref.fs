module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let myInt: Val = FInt 42L
let my_data: Val = myInt
