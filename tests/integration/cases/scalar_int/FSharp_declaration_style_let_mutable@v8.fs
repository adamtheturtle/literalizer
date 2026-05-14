module Main

type Val =
    | FInt of int64
let mutable my_data: Val = FInt 42L
