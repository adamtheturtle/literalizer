import std.json;
void main() {
int process(T...)(T args) { return 0; }
process(JSONValue(["a": JSONValue(1), "b": JSONValue(2)]));
}
