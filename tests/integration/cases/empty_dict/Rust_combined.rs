use std::collections::HashMap;
fn main() {
    {
        let my_data: HashMap<&str, &str> = HashMap::from([]);
        let _ = my_data;
    }
    let my_data: HashMap<&str, &str>;
    my_data = HashMap::from([]);
    let _ = my_data;
}
