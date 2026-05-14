import std.json;
void main() {
auto my_data = JSONValue([
    "metrics": JSONValue(["count": JSONValue(100), "rate": JSONValue(50)]),
    "flags": JSONValue(["retries": JSONValue(3), "timeout": JSONValue(30)]),
]);
}
