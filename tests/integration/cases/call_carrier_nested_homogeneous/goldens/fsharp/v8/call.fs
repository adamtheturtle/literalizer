module Main

type ClientType_() =
    member _.go(_first_value: obj, _second_value: obj) : obj = null
type AppType_() =
    member _.client = ClientType_()
let app = AppType_()
type Val =
    | FInt of int64
    | FList of Val list
app.client.go(FList [FInt 1L], FList [FInt 2L]) |> ignore
