module Main

open System.Text.Json.Nodes
let consume (_value: obj) : obj = null
let shared: JsonNode = null
consume((JsonObject(dict [("left", (if isNull shared then null else (shared).DeepClone())); ("nested", (JsonArray([|(if isNull shared then null else (shared).DeepClone())|]) :> JsonNode))]) :> JsonNode)) |> ignore
