import std.json;
void main() {
int process(T...)(T args) { return 0; }
auto unknown_value = parseJSON("[]");
process(JSONValue([unknown_value]));
}
