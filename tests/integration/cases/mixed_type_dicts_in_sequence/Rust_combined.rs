use std::collections::HashMap;
fn main() {
    let mut my_data = vec![
        HashMap::from([("type", "create"), ("pr_id", "pr_1"), ("draft", "True")]),
        HashMap::from([("type", "create"), ("pr_id", "pr_2")]),
    ];
    my_data = vec![
        HashMap::from([("type", "create"), ("pr_id", "pr_1"), ("draft", "True")]),
        HashMap::from([("type", "create"), ("pr_id", "pr_2")]),
    ];
    let _ = my_data;
}
