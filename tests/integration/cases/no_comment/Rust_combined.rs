use std::collections::HashMap;
fn main() {
    {
        let my_data = HashMap::from([
            ("message", "no comment here"),
        ]);
        let _ = my_data;
    }
    let my_data;
    my_data = HashMap::from([
        ("message", "no comment here"),
    ]);
    let _ = my_data;
}
