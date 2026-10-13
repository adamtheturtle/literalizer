use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    let bound = 2;
    let my_data = HashMap::from([
        ("value", bound),
    ]);
    let _ = &my_data;
}
