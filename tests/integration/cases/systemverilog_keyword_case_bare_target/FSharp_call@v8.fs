module Main

let Before (_value: obj) : obj = null
type Val =
    | FInt of int64
Before(FInt 1L) |> ignore
