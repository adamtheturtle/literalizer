import std.json;
void main() {
auto my_data = JSONValue([
    // before	line
    "value": JSONValue("left\tright"),  // inline	line
    // after	line
]);
}
