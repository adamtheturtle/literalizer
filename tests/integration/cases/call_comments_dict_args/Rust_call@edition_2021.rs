use std::collections::HashMap;
fn main() {
    fn process<A>(_value: A) {}
    // Test cases
    process(HashMap::from([("type", "create"), ("pr_id", "pr_1")]));  // first case
    process(HashMap::from([("type", "update"), ("pr_id", "pr_2")]));  // second case
    // third case
    process(HashMap::from([("type", "delete"), ("pr_id", "pr_3")]));
}
