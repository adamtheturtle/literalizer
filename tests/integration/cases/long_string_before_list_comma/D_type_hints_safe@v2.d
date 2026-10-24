import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue("This long string keeps its structural comma beyond the Fortran wrapping window without a safe split."),
    JSONValue(1),
]);
}
