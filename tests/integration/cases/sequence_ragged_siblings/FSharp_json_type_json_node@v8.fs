module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonArray([|
    (JsonArray([|(JsonValue.Create("set_task") :> JsonNode); (JsonValue.Create("web") :> JsonNode); (JsonValue.Create("lint_web") :> JsonNode)|]) :> JsonNode);
    (JsonArray([|(JsonValue.Create("merge_pipelines") :> JsonNode)|]) :> JsonNode)
|])
