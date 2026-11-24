use std::collections::HashMap;
fn main() {
    let mut my_data = vec![
        HashMap::from([("a", 1)]),
        <HashMap<&str, i32>>::from([]),
    ];
    let _ = &mut my_data;
}
