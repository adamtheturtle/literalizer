module Main

let first_value (_value: obj) : obj = null
type Val =
    | FInt of int64
first_value(FInt 1L) |> ignore
