import std.json;
void main() {
int process(T...)(T args) { return 0; }
auto untyped_value = parseJSON("[]");
process(JSONValue([untyped_value, untyped_value]));
}
