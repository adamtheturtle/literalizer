use std::collections::HashMap;
use std::collections::HashSet;
fn main() {
    let my_data = HashMap::from([
        ("key\nwith\nnewlines", "value1"),
        ("key\twith\ttabs", "value2"),
        ("", "value3"),
    ]);
    let _ = my_data;
}
