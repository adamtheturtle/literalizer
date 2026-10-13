use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    let my_data = HashMap::from([
        (1, "one"),
        (2, "two"),
        (42, "answer"),
    ]);
    let _ = &my_data;
}
