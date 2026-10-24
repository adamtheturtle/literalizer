import std.json;
void main() {
auto my_data = JSONValue([
    "fffe": JSONValue("￾"),
    "ffff": JSONValue("￿"),
]);
}
