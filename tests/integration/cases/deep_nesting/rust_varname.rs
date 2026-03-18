use std::collections::HashMap;
use std::collections::HashSet;
fn main() {
    let my_data = HashMap::from([
        ("level1", HashMap::from([("level2", HashMap::from([("level3", HashMap::from([("level4", HashMap::from([("value", "deep"), ("items", vec!["a", "b"])]))])), ("sibling", 42)])), ("tags", vec![HashMap::from([("name", "tag1"), ("meta", HashMap::from([("priority", 1), ("labels", vec!["x", "y"])]))])])])),
    ]);
    let _ = my_data;
}
