use std::collections::HashMap;
fn main() {
    let my_data = vec![
        HashMap::from([("mapping", HashMap::<String, String>::from([]))]),
        <HashMap<&str, HashMap<String, String>>>::from([]),
    ];
    let _ = my_data;
}
