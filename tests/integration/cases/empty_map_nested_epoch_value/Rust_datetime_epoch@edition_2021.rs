use std::collections::HashMap;
fn main() {
    let my_data = vec![
        HashMap::from([("nested", HashMap::from([("times", vec![-2208988800i64])]))]),
        <HashMap<&str, HashMap<&str, Vec<i64>>>>::from([]),
    ];
    let _ = &my_data;
}
