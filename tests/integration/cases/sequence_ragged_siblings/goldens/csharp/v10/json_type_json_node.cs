using System.Text.Json.Nodes;
JsonNode? my_data = new JsonArray {
    new JsonArray {"set_task", "web", "lint_web"},
    new JsonArray {"merge_pipelines"}
};
    _ = my_data;
