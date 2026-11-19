use serde_json::to_value;
fn main() {
    let item = Vec::<String>::new();
    let my_data = vec![
        item.clone(),
        item.clone(),
    ];
    if to_value(my_data.clone()).unwrap() != serde_json::from_str::<serde_json::Value>("[[], []]").unwrap() { std::process::exit(1); };
}
