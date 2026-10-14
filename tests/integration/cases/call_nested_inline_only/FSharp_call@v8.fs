module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
let f (_a: obj, _b: obj) : obj = null
f(FInt 2L, FStr "hello") |> ignore  // trailing note
f(FInt 3L, FStr "world") |> ignore  // another note
