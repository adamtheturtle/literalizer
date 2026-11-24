import std.json;
struct Record0 { JSONValue input; }
void main() {
auto my_data = [
    Record0(
        JSONValue([
            "a": JSONValue(1),
        ]),
    ),
    Record0(
        JSONValue([
            "b": JSONValue(2),
        ]),
    ),
];
}
