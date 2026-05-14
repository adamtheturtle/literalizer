use std::collections::HashMap;
fn main() {
    let mut my_data = HashMap::from([
        ("key\nwith\nnewlines", "value1"),
        ("key\twith\ttabs", "value2"),
        ("", "value3"),
    ]);
    my_data = HashMap::from([
        ("key\nwith\nnewlines", "value1"),
        ("key\twith\ttabs", "value2"),
        ("", "value3"),
    ]);
    let _ = my_data;
}
