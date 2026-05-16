use std::collections::HashMap;
use std::collections::HashSet;
struct Record0 {
    id: i32,
    empty_map: HashMap<String, String>,
    int_map: HashMap<i32, &'static str>,
    full_set: HashSet<&'static str>,
    empty_set: HashSet<String>,
}
fn main() {
    let my_data = vec![
        Record0 { id: 1, empty_map: HashMap::<String, String>::from([]), int_map: HashMap::from([(1, "a")]), full_set: HashSet::from(["x", "y"]), empty_set: HashSet::<String>::new() },
        Record0 { id: 2, empty_map: HashMap::<String, String>::from([]), int_map: HashMap::from([(1, "b")]), full_set: HashSet::from(["x"]), empty_set: HashSet::<String>::new() },
    ];
    let _ = my_data;
}
