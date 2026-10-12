use std::collections::HashMap;
fn main() {
    let mut shared = vec![
        1,
        2,
    ];
    let mut my_data = HashMap::from([
        ("a", shared.clone()),
    ]);
    my_data = HashMap::from([
        ("a", shared.clone()),
    ]);
    let _ = my_data;
}
