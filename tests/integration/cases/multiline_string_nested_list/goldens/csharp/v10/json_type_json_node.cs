using System.Text.Json.Nodes;
JsonNode? my_data = new JsonArray {
    new JsonArray {"\nfirst line\n  indented\n\nlast line\n"}
};
    _ = my_data;
