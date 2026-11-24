module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
type WorkerType_() =
    member _.``process``(_values: obj, _count: obj) : obj = null
type ApiType_() =
    member _.worker = WorkerType_()
let api = ApiType_()
api.worker.``process``(FList [FInt 1L; FMap []], FInt 42L) |> ignore
api.worker.``process``(FList [FInt 2L; FMap [("x", FStr "s")]], FInt 43L) |> ignore
