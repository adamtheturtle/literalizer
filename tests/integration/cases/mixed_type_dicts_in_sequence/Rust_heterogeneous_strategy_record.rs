use std::collections::HashMap;
struct Record0 {
    type: &'static str,
    pr_id: &'static str,
    draft: bool,
}
struct Record1 {
    type: &'static str,
    pr_id: &'static str,
}
fn main() {
    let my_data = vec![
        Record0 { type: "create", pr_id: "pr_1", draft: true },
        Record1 { type: "create", pr_id: "pr_2" },
    ];
    let _ = my_data;
}
