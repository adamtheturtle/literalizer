module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonObject(dict [
    ("exact_millisecond", (JsonValue.Create("09:30:15.123000") :> JsonNode));
    ("sub_millisecond", (JsonValue.Create("09:30:15.123456") :> JsonNode))
])
