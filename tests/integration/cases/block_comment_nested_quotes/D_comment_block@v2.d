import std.json;
void main() {
auto my_data = JSONValue([
    /* "{-" and '{-' stay readable */
    /* balanced {- nested -} and trailing -} stay readable */
    "x": JSONValue(1),
]);
}
