module Main

open System.Text.Json.Nodes
let ``process`` (_data: obj) : obj = null
let untypedValue: JsonNode = JsonArray()
``process``((JsonArray([|(if isNull untypedValue then null else (untypedValue).DeepClone()); (if isNull untypedValue then null else (untypedValue).DeepClone())|]) :> JsonNode)) |> ignore
