use std::collections::HashMap;
fn main() {
    let my_data = vec![
        HashMap::from([("type", "create"), ("pr_id", "pr_1"), ("draft", "True")]),
        HashMap::from([("type", "create"), ("pr_id", "pr_2"), ("draft", "None")]),
    ];
    let _ = my_data;
}
