use std::collections::HashMap;
use std::collections::HashSet;
fn main() {
    {
        let my_data = HashMap::from([
            ("users", vec![HashMap::from([("name", "Bob"), ("tags", vec!["admin", "user"])]), HashMap::from([("name", "Carol"), ("tags", vec!["guest"])])]),
        ]);
        let _ = my_data;
    }
    let my_data;
    my_data = HashMap::from([
        ("users", vec![HashMap::from([("name", "Bob"), ("tags", vec!["admin", "user"])]), HashMap::from([("name", "Carol"), ("tags", vec!["guest"])])]),
    ]);
    let _ = my_data;
}
