module Main

let make_widget (_value: obj) : obj = null
open System.Text.Json.Nodes
make_widget((JsonArray() :> JsonNode)) |> ignore
