use std::collections::HashMap;
fn main() {
    let my_data = vec![
        HashMap::from([("nested", HashMap::from([("times", vec!["1900-01-01T00:00:00+00:00"])]))]),
        <HashMap<&str, HashMap<&str, Vec<&str>>>>::from([]),
    ];
    let _ = &my_data;
}
