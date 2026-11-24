module Main

type Val =
    | FNull
    | FInt of int64
    | FList of Val list
let ``process`` (_value: obj) : obj = null
``process``(FNull) |> ignore
``process``(FList [FInt 1L; FInt 2L]) |> ignore
