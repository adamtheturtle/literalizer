use std::collections::HashMap;
fn main() {
    let my_data = vec![
        HashMap::from([("timestamp", "2020-01-01T00:00:00+00:00")]),
        <HashMap<&str, &str>>::from([]),
    ];
    let _ = my_data;
}
