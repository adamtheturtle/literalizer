using System.Text.Json.Nodes;
JsonNode? my_data = new JsonObject {
    ["outer"] = new JsonArray {new JsonArray {"nested first line\n  indented\n\nnested last line\n"}}
};
    _ = my_data;
