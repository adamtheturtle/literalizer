use std::collections::HashMap;
fn main() {
    let mut my_data = HashMap::from([
        ("key", "\"bang!\""),  // real
    ]);
    let _ = &my_data;
    my_data = HashMap::from([
        ("key", "\"bang!\""),  // real
    ]);
    let _ = &mut my_data;
}
