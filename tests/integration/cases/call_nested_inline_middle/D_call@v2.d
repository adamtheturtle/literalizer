import std.json;
void main() {
int f(T...)(T args) { return 0; }
f(JSONValue([JSONValue([JSONValue("DEL"), JSONValue("b"), JSONValue("10")]), JSONValue([JSONValue("ADD"), JSONValue("a"), JSONValue("x")])]));  // note
}
