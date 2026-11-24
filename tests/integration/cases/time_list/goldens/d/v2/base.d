import std.json;
void main() {
auto my_data = JSONValue([
    "times": JSONValue([JSONValue("09:30:00"), JSONValue("17:45:00"), JSONValue("23:59:59")]),
]);
}
