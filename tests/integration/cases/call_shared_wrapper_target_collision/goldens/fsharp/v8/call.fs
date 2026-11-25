module Main

let check (_value: obj) : obj = null
type Val =
    | FInt of int64
check(FInt 42L) |> ignore
