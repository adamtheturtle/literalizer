use std::collections::HashMap;
use std::collections::HashSet;
fn main() {
    let my_data = HashMap::from([
        ("key\nwith\nnewlines", "value1"),
        ("key	with	tabs", "value2"),
    ]);
    let _ = my_data;
}
