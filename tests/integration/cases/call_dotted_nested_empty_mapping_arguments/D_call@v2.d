import std.json;
void main() {
struct WorkerType_ { int process(T...)(T args) { return 0; } }
struct ApiType_ { WorkerType_ worker; }
ApiType_ api;
api.worker.process(JSONValue([JSONValue(1), parseJSON("{}")]), 42);
api.worker.process(JSONValue([JSONValue(2), JSONValue(["x": JSONValue("s")])]), 43);
}
