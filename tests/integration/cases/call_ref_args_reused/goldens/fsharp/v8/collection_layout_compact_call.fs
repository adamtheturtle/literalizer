module Main

type Val =
    | FInt of int64
    | FList of Val list
let ``process`` (_data: obj, _count: obj) : obj = null
let single_var: Val = FList [
    FInt 4L;
    FInt 5L;
    FInt 6L
]
let repeated_var: Val = FInt 1L
``process``(repeated_var, FInt 1L) |> ignore
``process``(single_var, FInt 0L) |> ignore
``process``(repeated_var, FInt 8L) |> ignore
