use std::collections::HashMap;
fn main() {
    let mut my_data = HashMap::from([
        ("key", "it's here"),  // a comment
    ]);
    my_data = HashMap::from([
        ("key", "it's here"),  // a comment
    ]);
    let _ = my_data;
}
