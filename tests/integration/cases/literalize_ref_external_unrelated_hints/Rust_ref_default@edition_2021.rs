use serde_json::to_value;
fn main() {
    let missing = vec![
        1,
        2,
    ];
    let my_data = missing;
    println!("{}", to_value(my_data.clone()).unwrap());
}
