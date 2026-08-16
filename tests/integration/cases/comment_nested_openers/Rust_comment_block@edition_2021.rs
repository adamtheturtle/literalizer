use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        /* nested openers / * and {- remain */
        ("x", 1),
    ]);
    let _ = my_data;
}
