module Main

type WorkerType_() =
    member _.``process``(_self: obj, _self_: obj) : obj = null
type ApiType_() =
    member _.worker = WorkerType_()
let api = ApiType_()
type Val =
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
api.worker.``process``(FMap [], FMap []) |> ignore
