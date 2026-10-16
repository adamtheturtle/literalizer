module Main

let make_widget (_value: obj) : obj = null
open System.Text.Json.Nodes
let my_data = make_widget((JsonArray([|(JsonValue.Create(1L) :> JsonNode)|]) :> JsonNode))
