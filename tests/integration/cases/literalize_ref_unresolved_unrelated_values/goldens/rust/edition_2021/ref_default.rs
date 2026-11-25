use serde_json::to_value;
fn main() {
    let a = 0;
    let my_data = vec![
        a,
        1,
    ];
    if to_value(my_data.clone()).unwrap() != serde_json::from_str::<serde_json::Value>("[0, 1]").unwrap() { std::process::exit(1); };
}
