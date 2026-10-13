use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    let my_data = HashMap::from([
        ("a", 1),  // tab	here and bidi <U+202E>after
        ("b", 2),
    ]);
    let _ = &my_data;
}
