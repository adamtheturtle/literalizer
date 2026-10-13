use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    let my_data = HashMap::from([
        ("key", "\"bang!\""),  // real
    ]);
    let _ = &my_data;
}
