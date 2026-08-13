using System.Text.Json.Nodes;
JsonNode? my_data = new JsonArray {
    new JsonObject {["first"] = "Alice", ["last"] = "Smith"},
    new JsonObject {["first"] = "Bob", ["last"] = "Jones"}
};
