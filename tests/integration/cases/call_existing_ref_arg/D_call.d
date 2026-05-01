import std.json;
void main() {
int send(T...)(T args) { return 0; }
auto existing = JSONValue(42);
send(existing);
}
