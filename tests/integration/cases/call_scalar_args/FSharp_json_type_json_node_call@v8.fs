module Main

open System.Text.Json.Nodes
let process (_value: obj) : obj = null
process((JsonValue.Create("hello") :> JsonNode))
process((JsonValue.Create(42L) :> JsonNode))
process((JsonValue.Create(true) :> JsonNode))
