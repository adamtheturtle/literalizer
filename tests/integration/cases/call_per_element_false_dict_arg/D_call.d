import std.json;
void main() {
int send(T...)(T args) { return 0; }
send(JSONValue(["a": JSONValue(1), "b": JSONValue("x")]));
}
