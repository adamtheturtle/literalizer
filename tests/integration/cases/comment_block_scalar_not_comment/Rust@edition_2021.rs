use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("description", "# not a comment\n"),
        ("name", "foo"),
    ]);
    let _ = my_data;
}
