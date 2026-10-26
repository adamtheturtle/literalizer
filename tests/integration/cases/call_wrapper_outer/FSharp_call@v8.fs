module Main

type Val =
    | FInt of int64
let ``process`` (_value: obj) : obj = null
let emit (__arg: obj) : obj = null
emit(``process``(FInt 42L)) |> ignore
