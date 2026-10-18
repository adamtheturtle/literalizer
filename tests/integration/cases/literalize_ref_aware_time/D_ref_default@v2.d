import std.json;
void main() {
auto shared_time = JSONValue("12:30:15+02:00");
auto my_data = JSONValue([
    "x": shared_time,
]);
}
