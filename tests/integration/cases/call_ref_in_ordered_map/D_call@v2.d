import std.json;
void main() {
int process(T...)(T args) { return 0; }
auto big_list = JSONValue([
    JSONValue("x"),
]);
process(JSONValue([JSONValue([JSONValue("m"), big_list])]));
}
