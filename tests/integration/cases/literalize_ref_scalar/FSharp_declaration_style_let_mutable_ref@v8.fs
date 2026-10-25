module Main

type Val =
    | FInt of int64
let mutable myInt: Val = FInt 42L
let mutable my_data: Val = myInt
