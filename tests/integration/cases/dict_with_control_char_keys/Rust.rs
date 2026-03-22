use std::collections::HashMap;
fn main() {
    let _ = HashMap::from([
        ("key\nwith\nnewlines", "value1"),
        ("key\twith\ttabs", "value2"),
        ("", "value3"),
    ]);
}
