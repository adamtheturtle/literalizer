use serde_json::to_value;
fn main() {
    let mut my_data = 0;
    let shared = 1;
    println!("{}", to_value(my_data.clone()).unwrap());
    my_data = shared;
    println!("{}", to_value(my_data.clone()).unwrap());
}
