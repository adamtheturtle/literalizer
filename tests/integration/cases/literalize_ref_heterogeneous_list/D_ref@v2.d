import std.json;
void main() {
auto one = JSONValue(1);
auto two = JSONValue("s");
auto my_data = JSONValue([
    one,
    two,
]);
}
