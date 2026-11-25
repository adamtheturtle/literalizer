module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonObject(dict [
    ("v", (JsonValue.Create("a﻿b") :> JsonNode))
])
