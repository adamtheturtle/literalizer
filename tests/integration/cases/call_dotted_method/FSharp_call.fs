module Check

type Val =
    | FBool of bool
    | FInt of int64
    | FStr of string
    | FList of Val list
type ClientType_() =
    member _.send(_payload: obj) : obj = null
type NsType_() =
    member _.client = ClientType_()
let ns = NsType_()
ns.client.send("hello")
ns.client.send(42)
ns.client.send(FBool true)
