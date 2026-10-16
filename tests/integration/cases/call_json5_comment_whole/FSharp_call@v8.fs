module Main

type Val =
    | FInt of int64
let f (_a: obj) : obj = null
// scalar heading
// second heading line
// scalar inline
// inline continuation
// scalar trailing
f(FInt 42L) |> ignore
