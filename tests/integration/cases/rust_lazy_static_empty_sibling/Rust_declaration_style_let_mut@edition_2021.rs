use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    #[allow(unused_mut)]
    let mut my_data = HashMap::from([
        ("a", vec![vec![1, 2], vec![3]]),
        ("b", vec![vec![], vec![1]]),
    ]);
    let _ = &mut my_data;
}
