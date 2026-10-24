module Main

type ObjType_() =
    member _.``class``(_a: obj) : obj = null
let obj = ObjType_()
type Val =
    | FInt of int64
obj.``class``(FInt 42L) |> ignore
