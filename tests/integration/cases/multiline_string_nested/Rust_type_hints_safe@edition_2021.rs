use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("outer", vec![vec!["nested first line\n  indented\n\nnested last line\n"]]),
    ]);
    let _ = &my_data;
}
