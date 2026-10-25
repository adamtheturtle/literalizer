module Main

open System.Text.Json.Nodes
let private _mainDeclaration () =
    let mutable shared: JsonNode = JsonArray([|
        (JsonValue.Create(1L) :> JsonNode);
        (JsonValue.Create(2L) :> JsonNode)
    |])
    let mutable my_data: JsonNode = JsonObject(dict [
        ("field", (if isNull shared then null else (shared).DeepClone()))
    ])
    ignore my_data

let private _mainAssignment () =
    let mutable shared: JsonNode = JsonArray([|
        (JsonValue.Create(1L) :> JsonNode);
        (JsonValue.Create(2L) :> JsonNode)
    |])
    let mutable my_data: JsonNode = JsonObject(dict [
        ("field", (if isNull shared then null else (shared).DeepClone()))
    ])
    let my_data: JsonNode = JsonObject(dict [
        ("field", (if isNull shared then null else (shared).DeepClone()))
    ])
    ignore my_data
