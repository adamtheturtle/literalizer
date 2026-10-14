module Main

type Val =
    | FInt of int64
type ObjType_() =
    member _.ZKV(_value: obj) : obj = null
let obj = ObjType_()
obj.ZKV(FInt 1L) |> ignore
