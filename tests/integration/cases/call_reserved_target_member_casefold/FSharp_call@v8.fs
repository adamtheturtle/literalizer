module Main

type ObjType_() =
    member _.BEGIN(_a: obj) : obj = null
let obj = ObjType_()
type Val =
    | FInt of int64
obj.BEGIN(FInt 42L)
