import std.json;
void main() {
struct WorkerType_ { int process(T...)(T args) { return 0; } }
struct ApiType_ { WorkerType_ worker; }
ApiType_ api;
api.worker.process(parseJSON("{}"), parseJSON("{}"));
}
