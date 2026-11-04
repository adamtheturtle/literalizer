import std.json;
void main() {
int f(T...)(T args) { return 0; }
f(JSONValue([JSONValue(1), JSONValue(2)]));
}
