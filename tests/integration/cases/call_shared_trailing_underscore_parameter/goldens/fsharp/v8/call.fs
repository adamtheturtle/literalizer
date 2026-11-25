module Main

let ``process`` (_value_: obj) : obj = null
type Val =
    | FInt of int64
    | FList of Val list
``process``(FInt 1L) |> ignore
