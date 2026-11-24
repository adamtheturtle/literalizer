module Main

let ``process`` (_i32: obj) : obj = null
type Val =
    | FInt of int64
    | FList of Val list
``process``(FInt 1L) |> ignore
