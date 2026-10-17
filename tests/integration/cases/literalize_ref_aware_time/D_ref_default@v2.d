import std.json;
void main() {
auto value = JSONValue("12:30:15+02:00");
auto my_data = JSONValue([
    "x": value,
]);
}
