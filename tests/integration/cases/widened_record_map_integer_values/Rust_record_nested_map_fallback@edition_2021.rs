use std::collections::HashMap;
#[derive(Clone)]
pub struct Record0 {
    pub input: HashMap<&'static str, i32>,
}
fn main() {
    let my_data = vec![
        Record0 { input: HashMap::from([("a", 1)]) },
        Record0 { input: HashMap::from([("b", 2)]) },
    ];
    let _ = &my_data;
}
