module Check

type Val =
    | FBool of bool
    | FInt of int64
    | FStr of string
    | FList of Val list
type ApiType_() =
    member _.request(_data: obj) : obj = null
type ClientType_() =
    member _.api = ApiType_()
let client = ClientType_()
client.api.request("hello")
client.api.request(42)
client.api.request(FBool true)
