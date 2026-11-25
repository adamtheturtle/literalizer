import std.json;
struct Record1 { string kind; string pr_id; }
struct Record0 { string name; Record1 input; JSONValue expected; }
void main() {
auto my_data = [
    Record0("test_1", Record1("create", "pr_1"), JSONValue(["pr_id": JSONValue("pr_1"), "status": JSONValue("draft")])),
    Record0("test_2", Record1("publish", "pr_1"), JSONValue(["error": JSONValue("invalid_operation")])),
];
}
