module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonObject(dict [
    ("quote\"backslash\\", (JsonValue.Create(1L) :> JsonNode));
    ("line\nbreak", (JsonValue.Create(2L) :> JsonNode));
    ("$(literal)${text}", (JsonValue.Create(3L) :> JsonNode));
    ("RStr prefix", (JsonValue.Create(4L) :> JsonNode))
])
