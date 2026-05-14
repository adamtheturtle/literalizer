import std.json;
void main() {
struct ClientType_ { int post(T...)(T args) { return 0; } }
struct ApiType_ { ClientType_ client; }
struct ObjType_ { ApiType_ api; }
ObjType_ obj;
obj.api.client.post("hello");
obj.api.client.post(42);
obj.api.client.post(true);
}
