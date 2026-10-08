module Main

type HelperType_() =
    member _.list(_a: obj) : obj = null
let helper = HelperType_()
type Val =
    | FInt of int64
    | FList of Val list
helper.list(FInt 1L)
