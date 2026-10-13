use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    let my_var = 1;
    let my_data = HashMap::from([
        ("key", my_var),
    ]);
    let _ = &my_data;
}
