module Main

type Val =
    | FInt of int64
    | FFloat of float
    | FList of Val list
let ``process`` (_value: obj) : obj = null
let emit (__call: obj, __zip: obj) : obj = null
emit(``process``(FInt 1L), FFloat 1.5) |> ignore
