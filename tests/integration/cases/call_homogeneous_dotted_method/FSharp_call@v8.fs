module Main

type Val =
    | FStr of string
    | FList of Val list
type ClientType_() =
    member _.fetch(_value: obj) : obj = null
type AppType_() =
    member _.client = ClientType_()
let app = AppType_()
app.client.fetch("hello")
app.client.fetch("world")
