module Main

type Val =
    | FInt of int64
type ObjType_() =
    member _.ZVal(_value: obj) : obj = null
let obj = ObjType_()
obj.ZVal(FInt 1L)
