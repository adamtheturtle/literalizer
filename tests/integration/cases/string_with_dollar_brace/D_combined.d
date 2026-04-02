import std.json;
void _check() {
auto my_data = JSONValue([
    JSONValue("prefix ${HOME} suffix"),
    JSONValue("${interpolated}"),
]);
my_data = JSONValue([
    JSONValue("prefix ${HOME} suffix"),
    JSONValue("${interpolated}"),
]);
}
