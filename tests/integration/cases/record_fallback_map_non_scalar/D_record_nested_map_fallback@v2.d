import std.json;
struct Record0 { string name; JSONValue payload; }
void main() {
auto my_data = [
    Record0("one", JSONValue(["scalar": JSONValue(1), "items": JSONValue([2, 3])])),
    Record0("two", JSONValue(["other": JSONValue(2)])),
];
}
