use std::collections::HashMap;
fn main() {
    let my_data = vec![
        HashMap::from([("timestamp", "2040-01-01T03:00:00+03:00")]),
        <HashMap<&str, &str>>::from([]),
    ];
    let _ = &my_data;
}
