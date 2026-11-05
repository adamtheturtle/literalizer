module Main

type Val =
    | FInt of int64
    | FList of Val list
let consume (_value: obj) : obj = null
consume(FInt 1L) |> ignore
