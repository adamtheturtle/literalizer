import std.json;
void main() {
int process(T...)(T args) { return 0; }
auto item = JSONValue([
    JSONValue(1),
    JSONValue(2),
]);
process(JSONValue([item, item]));
}
