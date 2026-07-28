import std.json;
void main() {
int process(T...)(T args) { return 0; }
auto my_list = JSONValue([
    "unused": JSONValue("value"),
]);
process(JSONValue([JSONValue([JSONValue(["inner": my_list])])]));
}
