use serde_json::to_value;
fn main() {
    let mut my_data = 0;
    let shared = 1;
    if to_value(my_data.clone()).unwrap() != serde_json::from_str::<serde_json::Value>("0").unwrap() { std::process::exit(1); };
    my_data = shared;
    if to_value(my_data.clone()).unwrap() != serde_json::from_str::<serde_json::Value>("1").unwrap() { std::process::exit(1); };
}
