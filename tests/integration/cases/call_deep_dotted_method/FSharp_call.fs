module Main

type Val =
    | FBool of bool
    | FInt of int64
    | FStr of string
    | FList of Val list
type ClientType_() =
    member _.post(_data: obj) : obj = null
type ApiType_() =
    member _.client = ClientType_()
type ObjType_() =
    member _.api = ApiType_()
let obj = ObjType_()
obj.api.client.post("hello")
obj.api.client.post(42)
obj.api.client.post(FBool true)
