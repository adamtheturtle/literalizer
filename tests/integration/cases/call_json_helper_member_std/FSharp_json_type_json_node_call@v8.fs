module Main

open System.Text.Json.Nodes
type ObjType_() =
    member _.std(_value: obj) : obj = null
let obj = ObjType_()
obj.std((JsonValue.Create(1L) :> JsonNode)) |> ignore
