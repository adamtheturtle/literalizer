use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        /* {- and {- stay readable */
        /* balanced {- nested -} and trailing -} stay readable */
        ("x", 1),
    ]);
    let _ = my_data;
}
