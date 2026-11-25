module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let consume (_value: obj) : obj = null
let item: Val = FInt 42L
consume(FMap [("field", item)]) |> ignore
