use std::collections::HashMap;
fn main() {
    let _ = HashMap::from([
        ("key", "value \" # not a comment"),  // real
    ]);
}
