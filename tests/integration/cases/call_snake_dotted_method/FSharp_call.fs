module Main

type Val =
    | FBool of bool
    | FInt of int64
    | FStr of string
    | FList of Val list
type Http_ClientType_() =
    member _.fetch(_payload: obj) : obj = null
type My_AppType_() =
    member _.http_client = Http_ClientType_()
let my_app = My_AppType_()
my_app.http_client.fetch("hello")
my_app.http_client.fetch(42)
my_app.http_client.fetch(FBool true)
