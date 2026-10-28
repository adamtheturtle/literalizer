import std.json;
void main() {
auto my_data = JSONValue([
    "user_name": JSONValue(1),
    "user.name": JSONValue(2),
    "user-name": JSONValue(3),
    "field_name_that_is_really_quite_long_one": JSONValue(4),
    "field_name_that_is_really_quite_long_two": JSONValue(5),
]);
}
