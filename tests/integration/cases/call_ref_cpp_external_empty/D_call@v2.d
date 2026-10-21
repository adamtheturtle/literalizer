import std.json;
void main() {
int consume(T...)(T args) { return 0; }
auto item = JSONValue([
    JSONValue(1),
    JSONValue(2),
]);
consume(item);
}
