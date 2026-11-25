module Main

open System.Text.Json.Nodes
let private _mainDeclaration () =
    let mutable shared: JsonNode = JsonArray([|
        (JsonValue.Create(1L) :> JsonNode);
        (JsonValue.Create(2L) :> JsonNode)
    |])
    let mutable my_data: JsonNode = shared
    ignore my_data

let private _mainAssignment () =
    let mutable shared: JsonNode = JsonArray([|
        (JsonValue.Create(1L) :> JsonNode);
        (JsonValue.Create(2L) :> JsonNode)
    |])
    let mutable my_data: JsonNode = shared
    let my_data: JsonNode = shared
    ignore my_data
