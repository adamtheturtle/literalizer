module Main

open System.Text.Json.Nodes
let ``process`` (_data: obj) : obj = null
let unknown_value: JsonNode = JsonArray()
``process``((JsonArray([|(if isNull unknown_value then null else (unknown_value).DeepClone())|]) :> JsonNode)) |> ignore
