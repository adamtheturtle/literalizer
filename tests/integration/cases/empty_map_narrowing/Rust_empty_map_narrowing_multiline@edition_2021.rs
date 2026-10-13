use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    let my_data = vec![
        <HashMap<&str, i32>>::from([]),
        HashMap::from([
            ("x", 1),
        ]),
    ];
    let _ = &my_data;
}
