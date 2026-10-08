use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("comma_hash", "a,#b"),
        ("comma_space_hash", "trail, # comment"),
        ("escaped_quote", "quote \" and , #"),
        ("next_line", "xy"),
        ("line_separator", "x y"),
        ("paragraph_separator", "x y"),
    ]);
    let _ = my_data;
}
