import std.json;
void main() {
int process(T...)(T args) { return 0; }
auto my_list = parseJSON("[]");
process(JSONValue([JSONValue([JSONValue(["inner": my_list])])]));
}
