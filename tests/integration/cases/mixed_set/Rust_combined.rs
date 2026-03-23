use std::collections::HashSet;
fn main() {
    {
        let my_data = HashSet::from([
            "42",
            "True",
            "apple",
        ]);
        let _ = my_data;
    }
    let my_data;
    my_data = HashSet::from([
        "42",
        "True",
        "apple",
    ]);
    let _ = my_data;
}
