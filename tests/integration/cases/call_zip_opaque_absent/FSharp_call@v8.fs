module Main

type Val =
    | FInt of int64
let ``process`` (_value: obj) : obj = null
``process``(FInt 1L) |> ignore
