function process() {}
// Test cases
process({ value: {"type": "create", "pr_id": "pr_1"} });  // first case
process({ value: {"type": "update", "pr_id": "pr_2"} });  // second case
// third case
process({ value: {"type": "delete", "pr_id": "pr_3"} });
