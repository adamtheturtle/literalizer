module Main

open System.Text.Json.Nodes
let consume (_value: obj) : obj = null
let shared: JsonNode = null
consume((JsonObject(dict [("left", (shared :> JsonNode)); ("nested", (JsonArray([|(shared :> JsonNode)|]) :> JsonNode))]) :> JsonNode)) |> ignore
