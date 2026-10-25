module Main

open System.Text.Json.Nodes
let ``process`` (_value: obj) : obj = null
let arena: JsonNode = JsonObject(dict [
    ("a", (JsonValue.Create(1L) :> JsonNode))
])
let ZVal: JsonNode = JsonObject(dict [
    ("a", (JsonValue.Create(1L) :> JsonNode))
])
let ZKV: JsonNode = JsonObject(dict [
    ("a", (JsonValue.Create(1L) :> JsonNode))
])
``process``(arena) |> ignore
``process``(ZVal) |> ignore
``process``(ZKV) |> ignore
