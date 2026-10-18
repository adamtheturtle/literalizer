import std.json;
void main() {
auto my_time = JSONValue("01:02:03");
auto my_data = JSONValue([
    "x": my_time,
]);
}
