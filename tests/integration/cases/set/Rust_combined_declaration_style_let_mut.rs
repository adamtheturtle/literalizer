use std::collections::HashSet;
fn main() {
    {
        let mut my_data = HashSet::from([
            "apple",
            "banana",
            "cherry",
        ]);
        let _ = my_data;
    }
    let my_data;
    my_data = HashSet::from([
        "apple",
        "banana",
        "cherry",
    ]);
    let _ = my_data;
}
