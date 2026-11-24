module Main

let ``process`` (_value: obj, __value: obj) : obj = null
type Val =
    | FInt of int64
    | FList of Val list
``process``(FInt 1L, FInt 2L) |> ignore
