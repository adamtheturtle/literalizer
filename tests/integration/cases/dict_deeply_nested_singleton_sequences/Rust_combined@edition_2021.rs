use std::collections::HashMap;
fn main() {
    let mut my_data = HashMap::from([
        ("deep", vec![vec![vec![vec![1]]]]),
    ]);
    my_data = HashMap::from([
        ("deep", vec![vec![vec![vec![1]]]]),
    ]);
    let _ = my_data;
}
