module Main

let ``process`` (_value: obj) : obj = null
type Val =
    | FNull
    | FBool of bool
    | FInt of int64
    | FStr of string
    | FList of Val list
``process``(FStr "hello") |> ignore
``process``(FInt 42L) |> ignore
``process``(FBool true) |> ignore
``process``(FNull) |> ignore
