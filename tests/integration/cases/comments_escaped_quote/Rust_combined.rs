use std::collections::HashMap;
fn main() {
    let mut my_data = HashMap::from([
        ("key", "value \" # not a comment"),  // real
    ]);
    my_data = HashMap::from([
        ("key", "value \" # not a comment"),  // real
    ]);
    let _ = my_data;
}
