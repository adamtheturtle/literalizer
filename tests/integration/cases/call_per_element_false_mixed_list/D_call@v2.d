import std.json;
void main() {
int process(T...)(T args) { return 0; }
process(JSONValue([JSONValue(1), JSONValue("x")]));
}
