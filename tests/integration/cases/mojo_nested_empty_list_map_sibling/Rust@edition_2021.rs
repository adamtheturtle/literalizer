use std::collections::HashMap;
fn main() {
    let my_data = vec![
        HashMap::from([("values", Vec::<String>::new())]),
        <HashMap<&str, Vec<String>>>::from([]),
    ];
    let _ = my_data;
}
