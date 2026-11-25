module Main

type ProcessType_() =
    member _.fetch(_data: obj) : obj = null
type AppType_() =
    member _.``process`` = ProcessType_()
let app = AppType_()
type Val =
    | FBool of bool
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
app.``process``.fetch(FMap [("data", FStr "hello")]) |> ignore
app.``process``.fetch(FMap [("data", FInt 42L)]) |> ignore
app.``process``.fetch(FMap [("data", FBool true)]) |> ignore
