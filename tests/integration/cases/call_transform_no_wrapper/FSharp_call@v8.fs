module Main

type Val =
    | FBool of bool
    | FInt of int64
    | FStr of string
    | FList of Val list
let ``process`` (_value: obj) : obj = null
``process``(FStr "hello") |> ignore
``process``(FInt 42L) |> ignore
``process``(FBool true) |> ignore
