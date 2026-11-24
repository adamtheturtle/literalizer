use std::collections::HashMap;
fn main() {
    let my_data = vec![
        HashMap::from([("value", Vec::new())]),
        HashMap::from([("value", vec![1])]),
    ];
    let _ = &my_data;
}
