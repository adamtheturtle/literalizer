module Main

let f (_a: obj) : obj = null
type Val =
    | FInt of int64
    | FList of Val list
f(FList [FList [FInt 1L; FInt 2L]; FList [FInt 3L]]) |> ignore
