module Main

type Val =
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
type ApiType_() =
    member _.``process``(_self: obj) : obj = null
let api = ApiType_()
api.``process``(FMap []) |> ignore
