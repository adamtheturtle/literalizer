module Main

let make_widget (_value: obj) : obj = null
open System.Text.Json.Nodes
make_widget((JsonValue.Create(1L) :> JsonNode)) |> ignore
