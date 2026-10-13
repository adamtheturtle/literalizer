use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    let my_data = HashMap::from([
        ("key", "it's here"),  // a comment
    ]);
    let _ = &my_data;
}
