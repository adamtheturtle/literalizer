use std::collections::HashMap;
fn main() {
    let my_data = (
        HashMap::from([("values", ())]),
        <HashMap<&str, ()>>::from([]),
    );
    let _ = &my_data;
}
