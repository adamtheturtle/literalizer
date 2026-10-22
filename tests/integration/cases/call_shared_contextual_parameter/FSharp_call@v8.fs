module Main

let ``process`` (_using: obj) : obj = null
type Val =
    | FInt of int64
    | FList of Val list
``process``(FInt 1L) |> ignore
