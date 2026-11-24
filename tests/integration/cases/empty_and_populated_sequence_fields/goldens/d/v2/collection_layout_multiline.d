import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([
        "value": parseJSON("[]"),
    ]),
    JSONValue([
        "value": JSONValue([
            JSONValue(1),
        ]),
    ]),
]);
my_data = JSONValue([
    JSONValue([
        "value": parseJSON("[]"),
    ]),
    JSONValue([
        "value": JSONValue([
            JSONValue(1),
        ]),
    ]),
]);
}
