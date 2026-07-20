module Main

let make_widget (_count: obj) : obj = null
open System.Text.Json.Nodes
let my_data = make_widget((JsonValue.Create(42L) :> JsonNode))
