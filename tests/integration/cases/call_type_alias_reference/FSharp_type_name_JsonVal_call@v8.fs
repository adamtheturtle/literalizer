module Main

type JsonVal =
    | FInt of int64
let ``process`` (_value: obj) : obj = null
let value: JsonVal = FInt 1L
``process``(value) |> ignore
