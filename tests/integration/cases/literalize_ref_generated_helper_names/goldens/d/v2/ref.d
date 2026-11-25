import std.json;
void main() {
auto std = JSONValue([
    "a": JSONValue(1),
]);
auto arena = JSONValue([
    "a": JSONValue(1),
]);
auto allocator = JSONValue([
    "a": JSONValue(1),
]);
auto my_data = JSONValue([
    std,
    arena,
    allocator,
]);
}
