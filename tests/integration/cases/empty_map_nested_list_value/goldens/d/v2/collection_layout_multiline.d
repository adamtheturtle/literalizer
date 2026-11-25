import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([
        JSONValue([
            "values": JSONValue([
                parseJSON("[]"),
            ]),
        ]),
        parseJSON("{}"),
    ]),
    JSONValue([
        parseJSON("{}"),
        JSONValue([
            "values": JSONValue([
                parseJSON("[]"),
            ]),
        ]),
    ]),
]);
}
