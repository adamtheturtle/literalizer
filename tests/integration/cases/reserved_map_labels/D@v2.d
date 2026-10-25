import std.json;
void main() {
auto my_data = JSONValue([
    "if": JSONValue(1),
    "then": JSONValue(2),
    "else": JSONValue(3),
    "let": JSONValue(4),
    "in": JSONValue(5),
    "using": JSONValue(6),
    "missing": JSONValue(7),
    "assert": JSONValue(8),
    "as": JSONValue(9),
    "Infinity": JSONValue(10),
    "NaN": JSONValue(11),
    "merge": JSONValue(12),
    "Some": JSONValue(13),
    "toMap": JSONValue(14),
    "forall": JSONValue(15),
    "with": JSONValue(16),
    "ordinary": JSONValue(17),
]);
}
