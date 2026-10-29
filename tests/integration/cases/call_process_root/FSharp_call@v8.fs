module Main

type ApiType_() =
    member _.fetch(_data: obj) : obj = null
type ProcessType_() =
    member _.api = ApiType_()
let ``process`` = ProcessType_()
type Val =
    | FBool of bool
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
``process``.api.fetch(FMap [("data", FStr "hello")]) |> ignore
``process``.api.fetch(FMap [("data", FInt 42L)]) |> ignore
``process``.api.fetch(FMap [("data", FBool true)]) |> ignore
