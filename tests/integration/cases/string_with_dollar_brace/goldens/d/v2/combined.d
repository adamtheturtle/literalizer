import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue("prefix ${HOME} suffix"),
    JSONValue("${interpolated}"),
]);
my_data = JSONValue([
    JSONValue("prefix ${HOME} suffix"),
    JSONValue("${interpolated}"),
]);
}
