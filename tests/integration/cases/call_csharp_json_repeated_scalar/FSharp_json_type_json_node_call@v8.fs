module Main

open System.Text.Json.Nodes
let consume (_value: obj) : obj = null
let shared: JsonNode = JsonValue.Create(42L)
consume((JsonArray([|(shared :> JsonNode); (shared :> JsonNode)|]) :> JsonNode)) |> ignore
