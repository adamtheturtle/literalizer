import std.json;
void main() {
auto my_data = JSONValue([
    "omap_value": JSONValue([
        JSONValue([JSONValue("first"), JSONValue(1)]),
    ]),
    "sibling_lists": JSONValue([
        "numbers": JSONValue([
            JSONValue(1),
            JSONValue(2),
        ]),
        "strings": JSONValue([
            JSONValue("x"),
            JSONValue("y"),
        ]),
    ]),
    "ref_marker_present": JSONValue([
        JSONValue("$keep"),
        JSONValue("z"),
    ]),
]);
}
