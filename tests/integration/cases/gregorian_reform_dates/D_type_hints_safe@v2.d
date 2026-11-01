import std.json;
void main() {
auto my_data = JSONValue([
    "ancient_date": JSONValue("1500-03-01"),
    "modern_date": JSONValue("2024-01-15"),
    "before_date": JSONValue("1582-10-04"),
    "gap_date": JSONValue("1582-10-10"),
    "transition_date": JSONValue("1582-10-15"),
    "after_date": JSONValue("1582-10-16"),
    "before_naive": JSONValue("1582-10-04T12:30:00.000001"),
    "gap_naive": JSONValue("1582-10-10T12:30:00.500000"),
    "transition_positive": JSONValue("1582-10-15T00:30:00+18:00"),
    "transition_negative": JSONValue("1582-10-15T23:30:00-18:00"),
    "after_positive": JSONValue("1582-10-16T00:30:00+18:00"),
]);
}
