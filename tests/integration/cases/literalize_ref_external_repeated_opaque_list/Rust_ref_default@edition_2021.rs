use serde_json::to_value;
fn main() {
    let item = Vec::<String>::new();
    let my_data = vec![
        item.clone(),
        item.clone(),
    ];
    println!("{}", to_value(my_data.clone()).unwrap());
}
