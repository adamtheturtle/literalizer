module Main

open System.Text.Json.Nodes
let consume (_value: obj) : obj = null
let shared: JsonNode = JsonValue.Create(42L)
consume((JsonArray([|(if isNull shared then null else (shared).DeepClone()); (if isNull shared then null else (shared).DeepClone())|]) :> JsonNode)) |> ignore
