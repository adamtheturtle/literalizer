use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    let my_data = HashMap::from([
        ("key", "value \" # not a comment"),  // real
    ]);
    let _ = &my_data;
}
