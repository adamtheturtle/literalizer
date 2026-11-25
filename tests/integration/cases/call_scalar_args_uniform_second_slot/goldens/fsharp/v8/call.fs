module Main

type Val =
    | FBool of bool
    | FInt of int64
    | FStr of string
    | FList of Val list
let ``process`` (_value: obj, _label: obj) : obj = null
``process``(FStr "hello", FStr "a") |> ignore
``process``(FInt 42L, FStr "b") |> ignore
``process``(FBool true, FStr "c") |> ignore
