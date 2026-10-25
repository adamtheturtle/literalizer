module Main

type Val =
    | FInt of int64
let consume (_value: obj) : obj = null
let mutable shared: Val = FInt 42L
consume(shared) |> ignore
