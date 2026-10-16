module Main

type Val =
    | FInt of int64
    | FList of Val list
let f (_a: obj, _b: obj) : obj = null
// calls heading
// before call one
// first argument
f(FInt 1L, FInt 2L) |> ignore  // after call one
// second argument
f(FInt 3L, FInt 4L) |> ignore
// after all calls
