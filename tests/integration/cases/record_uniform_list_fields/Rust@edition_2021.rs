use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    let my_data = vec![
        HashMap::from([("scores", vec![1, 2])]),
        HashMap::from([("scores", vec![3, 4])]),
    ];
    let _ = &my_data;
}
