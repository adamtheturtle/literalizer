using System.Text.Json.Nodes;
JsonNode? my_data = new JsonArray {
    "C:\\path\\to\\file",
    "back\\\\slash",
    "hello \\\"world\\\"",
    "path\\to \"# file",
    "trailing\\",
    "both \"quotes''' here",
    "line1\\nline2\nwith newline"
};
    _ = my_data;
