use serde_json::to_value;
fn main() {
    let a = 0;
    let my_data = vec![
        a,
        1,
    ];
    println!("{}", to_value(my_data.clone()).unwrap());
}
