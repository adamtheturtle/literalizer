use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    let my_data = HashMap::from([
        ("a", Vec::<String>::new()),
        ("b", Vec::<String>::new()),
    ]);
    let _ = &my_data;
}
