use std::collections::HashMap;
use std::collections::HashSet;
fn main() {
    {
        let my_data = HashMap::from([
            ("a", 1),
            ("b", 2.5),
            ("c", 3),
        ]);
        let _ = my_data;
    }
    let my_data;
    my_data = HashMap::from([
        ("a", 1),
        ("b", 2.5),
        ("c", 3),
    ]);
    let _ = my_data;
}
