module Main

type Val =
    | FInt of int64
    | FList of Val list
let ``process`` (_value: obj) : obj = null
let emit (__call: obj, __zip: obj) : obj = null
emit(``process``(FInt 1L), FInt 1705320000L) |> ignore
