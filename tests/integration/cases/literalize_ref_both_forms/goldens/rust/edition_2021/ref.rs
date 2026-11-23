use std::collections::HashMap;
fn main() {
    let mut shared_values = vec![
        1,
        2,
    ];
    let _ = &mut shared_values;
    let mut my_data = HashMap::from([
        ("a", shared_values.clone()),
    ]);
    let _ = &my_data;
    my_data = HashMap::from([
        ("a", shared_values.clone()),
    ]);
    let _ = &mut my_data;
}
