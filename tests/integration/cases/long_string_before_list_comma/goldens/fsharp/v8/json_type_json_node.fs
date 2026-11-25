module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonArray([|
    (JsonValue.Create("This long string keeps its structural comma beyond the Fortran wrapping window without a safe split.") :> JsonNode);
    (JsonValue.Create(1L) :> JsonNode)
|])
