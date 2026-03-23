use std::collections::HashMap;
fn main() {
    {
        let my_data = HashMap::from([
            ("a", "{\"x\": 1}"),
            ("b", "2"),
        ]);
        let _ = my_data;
    }
    let my_data;
    my_data = HashMap::from([
        ("a", "{\"x\": 1}"),
        ("b", "2"),
    ]);
    let _ = my_data;
}
