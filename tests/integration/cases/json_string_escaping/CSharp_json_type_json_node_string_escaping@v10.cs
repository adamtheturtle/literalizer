using System.Text.Json.Nodes;
JsonNode? my_data = new JsonObject {
    ["$key"] = "a\"b\tcé #{world} $ident",
    ["trailing multi-byte"] = "café"
};
