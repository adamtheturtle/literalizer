class Process_ {
    construct new() {}
    call(value) {}
}
var process = Process_.new()
// Test cases
process.call({"type": "create", "pr_id": "pr_1"})  // first case
process.call({"type": "update", "pr_id": "pr_2"})  // second case
// third case
process.call({"type": "delete", "pr_id": "pr_3"})
