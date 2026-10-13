use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    let my_data = HashMap::from([
        (1, (1, "email", "a@gmail.com", 100)),
    ]);
    let _ = &my_data;
}
