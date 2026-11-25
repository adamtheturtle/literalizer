import std.json;
void main() {
auto my_data = JSONValue([
    "half": JSONValue("1979-05-27T07:32:00.500000"),
    "milli": JSONValue("1979-05-27T07:32:00.100000"),
    "max_milli": JSONValue("1979-05-27T07:32:00.999000"),
    "whole": JSONValue("1979-05-27T07:32:00"),
]);
}
