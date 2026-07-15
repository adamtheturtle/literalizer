import std.json;
struct Record0 { string name; JSONValue input; JSONValue expected; }
void main() {
auto my_data = [
    Record0(
        "test_1",
        JSONValue([
            "type": JSONValue("create"),
            "pr_id": JSONValue("pr_1"),
            "draft": JSONValue(true),
        ]),
        JSONValue([
            "pr_id": JSONValue("pr_1"),
            "status": JSONValue("draft"),
        ]),
    ),
    Record0(
        "test_2",
        JSONValue([
            "type": JSONValue("publish"),
            "pr_id": JSONValue("pr_1"),
        ]),
        JSONValue([
            "error": JSONValue("invalid_operation"),
        ]),
    ),
];
}
