module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonArray([|
    (JsonValue.Create("C:\\path\\to\\file") :> JsonNode);
    (JsonValue.Create("back\\\\slash") :> JsonNode);
    (JsonValue.Create("hello \\\"world\\\"") :> JsonNode);
    (JsonValue.Create("path\\to \"# file") :> JsonNode);
    (JsonValue.Create("trailing\\") :> JsonNode);
    (JsonValue.Create("both \"quotes''' here") :> JsonNode);
    (JsonValue.Create("line1\\nline2\nwith newline") :> JsonNode)
|])
