module Main

type ObjType_() =
    member _.ZVal(__arg: obj) : obj = null
let obj = ObjType_()
type Val =
    | FInt of int64
let my_data = obj.ZVal(FInt 42L) // note
