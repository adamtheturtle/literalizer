use std::collections::HashSet;
#[allow(non_snake_case)]
fn main() {
    let my_data = HashSet::from([
        "1969-12-31T23:59:59+00:00",
    ]);
    let _ = &my_data;
}
