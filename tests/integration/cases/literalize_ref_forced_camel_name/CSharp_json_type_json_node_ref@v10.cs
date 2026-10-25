using System.Text.Json.Nodes;
JsonNode? userObj = new JsonObject {
    ["_"] = "_"
};
JsonNode? my_data = ((JsonNode?)userObj)?.DeepClone();
    _ = my_data;
