module Main

type Val =
    | FInt of int64
let ``process`` (_value: obj) : obj = null
let value: Val = FInt 1L
``process``(value) |> ignore
