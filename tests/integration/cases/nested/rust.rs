use std::collections::HashMap;
use std::collections::HashSet;
fn main() {
    let _ = HashMap::from([(
        "users",
        vec![
            HashMap::from([("name", "Bob"), ("tags", vec!["admin", "user"])]),
            HashMap::from([("name", "Carol"), ("tags", vec!["guest"])]),
        ],
    )]);
}
