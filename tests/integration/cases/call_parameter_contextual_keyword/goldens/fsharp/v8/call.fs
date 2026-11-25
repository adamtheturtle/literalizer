module Main

let f (_using: obj) : obj = null
type Val =
    | FInt of int64
    | FList of Val list
f(FInt 1L) |> ignore
