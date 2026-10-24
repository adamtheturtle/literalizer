import std.json;
void main() {
auto my_data = JSONValue([
    "quote\"backslash\\": JSONValue(1),
    "line\nbreak": JSONValue(2),
    "$(literal)${text}": JSONValue(3),
    "RStr prefix": JSONValue(4),
]);
}
