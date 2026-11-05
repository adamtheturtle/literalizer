import std.json;
void main() {
int process(T...)(T args) { return 0; }
process(null);
process(JSONValue([JSONValue(1), JSONValue(2)]));
}
