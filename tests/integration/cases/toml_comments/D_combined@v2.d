import std.json;
void main() {
auto my_data = JSONValue([
    // before
    "answer": JSONValue(42),  // inline
    "plain": JSONValue("ok"),
    // trailing
]);
my_data = JSONValue([
    // before
    "answer": JSONValue(42),  // inline
    "plain": JSONValue("ok"),
    // trailing
]);
}
