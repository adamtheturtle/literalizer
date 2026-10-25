module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let ``process`` (_values: obj, _count: obj) : obj = null
``process``(FList [FInt 1L; FMap []], FInt 42L) |> ignore
