use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        // before	line
        ("value", "left\tright"),  // inline	line
        // after	line
    ]);
    let _ = &my_data;
}
