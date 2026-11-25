module Main

let consume (_value: obj) : obj = null
type Val =
    | FList of Val list
    | FInt of int64
consume(FInt(-2147483649L)) |> ignore
consume(FInt 2147483648L) |> ignore
