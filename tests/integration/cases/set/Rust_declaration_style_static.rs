use std::collections::HashSet;
fn main() {
    static my_data: HashSet<&str> = HashSet::from([
        "apple",
        "banana",
        "cherry",
    ]);
    let _ = my_data;
}
