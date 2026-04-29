dynamic process({dynamic value}) => null;
final my_data = null;
void main() {
    // Test cases
    process(value: <String, String>{"type": "create", "pr_id": "pr_1"});  // first case
    process(value: <String, String>{"type": "update", "pr_id": "pr_2"});  // second case
    // third case
    process(value: <String, String>{"type": "delete", "pr_id": "pr_3"});
}
