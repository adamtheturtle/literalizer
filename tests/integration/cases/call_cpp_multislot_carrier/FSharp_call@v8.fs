module Main

let ``process`` (_value: obj, _extra: obj) : obj = null
type Val =
    | FNull
    | FBool of bool
    | FInt of int64
    | FFloat of float
    | FStr of string
    | FList of Val list
``process``(FInt 1L, FStr "hello") |> ignore
``process``(FStr "two", FBool false) |> ignore
``process``(FFloat 3.5, FNull) |> ignore
