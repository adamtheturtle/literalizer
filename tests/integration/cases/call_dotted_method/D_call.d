import std.json;
void _check() {
struct ClientType_ { int send(T...)(T args) { return 0; } }
struct NsType_ { ClientType_ client; }
NsType_ ns;
ns.client.send("hello");
ns.client.send(42);
ns.client.send(true);
}
