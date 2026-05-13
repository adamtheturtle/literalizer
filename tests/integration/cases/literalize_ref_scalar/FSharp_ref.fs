module Main

type Val =
    | FInt of int64
let myInt: Val = FInt 42L
let my_data: Val = myInt
