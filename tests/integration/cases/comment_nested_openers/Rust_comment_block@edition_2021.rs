use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    let my_data = HashMap::from([
        /* nested openers / * and {- remain */
        ("x", 1),
    ]);
    let _ = &my_data;
}
