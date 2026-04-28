module Main

type Val =
    | FBool of bool
    | FInt of int64
    | FStr of string
    | FList of Val list
type ClientType_() =
    member _.fetch(_payload: obj) : obj = null
type AppType_() =
    member _.client = ClientType_()
let app = AppType_()
let emit (__arg: obj) : obj = null
emit(app.client.fetch("hello"))
emit(app.client.fetch(42))
emit(app.client.fetch(FBool true))
