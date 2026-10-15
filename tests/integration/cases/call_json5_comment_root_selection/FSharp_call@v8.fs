module Main

type Val =
    | FInt of int64
    | FList of Val list
let f (_a: obj, _b: obj) : obj = null
// selected heading
f(FInt 1L, FInt 2L) |> ignore  // selected inline
