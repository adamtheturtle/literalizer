import std.json;
void main() {
auto my_data = JSONValue([
    "exact_millisecond": JSONValue("09:30:15.123000"),
    "sub_millisecond": JSONValue("09:30:15.123456"),
]);
}
