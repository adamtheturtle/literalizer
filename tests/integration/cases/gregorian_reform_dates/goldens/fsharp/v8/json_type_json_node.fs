module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonObject(dict [
    ("ancient_date", (JsonValue.Create("1500-03-01") :> JsonNode));
    ("modern_date", (JsonValue.Create("2024-01-15") :> JsonNode));
    ("before_date", (JsonValue.Create("1582-10-04") :> JsonNode));
    ("gap_date", (JsonValue.Create("1582-10-10") :> JsonNode));
    ("transition_date", (JsonValue.Create("1582-10-15") :> JsonNode));
    ("after_date", (JsonValue.Create("1582-10-16") :> JsonNode));
    ("before_naive", (JsonValue.Create("1582-10-04T12:30:00.000001") :> JsonNode));
    ("gap_naive", (JsonValue.Create("1582-10-10T12:30:00.500000") :> JsonNode));
    ("transition_positive", (JsonValue.Create("1582-10-15T00:30:00+18:00") :> JsonNode));
    ("transition_negative", (JsonValue.Create("1582-10-15T23:30:00-18:00") :> JsonNode));
    ("after_positive", (JsonValue.Create("1582-10-16T00:30:00+18:00") :> JsonNode))
])
