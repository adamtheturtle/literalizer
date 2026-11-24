import std.json;
void main() {
auto my_var = JSONValue(1);
auto my_data = JSONValue([
    "key": my_var,
]);
}
