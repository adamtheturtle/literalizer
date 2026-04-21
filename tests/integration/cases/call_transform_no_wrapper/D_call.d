import std.json;
void _check() {
struct ApiType_ { int request(T...)(T args) { return 0; } }
struct ClientType_ { ApiType_ api; }
ClientType_ client;
client.api.request("hello");
client.api.request(42);
client.api.request(true);
}
