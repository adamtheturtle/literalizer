use serde_json::to_value;
fn main() {
    let missing = vec![
        1,
        2,
    ];
    let my_data = missing;
    if to_value(my_data.clone()).unwrap() != serde_json::from_str::<serde_json::Value>("[1, 2]").unwrap() { std::process::exit(1); };
}
