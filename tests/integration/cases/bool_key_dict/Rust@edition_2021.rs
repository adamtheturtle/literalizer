use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    let my_data = HashMap::from([
        (true, "yes"),
        (false, "no"),
    ]);
    let _ = &my_data;
}
