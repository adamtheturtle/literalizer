use std::collections::HashMap;
fn main() {
    {
        let my_data = HashMap::from([
            ("key", "value \" # not a comment"),  // real
        ]);
        let _ = my_data;
    }
    let my_data;
    my_data = HashMap::from([
        ("key", "value \" # not a comment"),  // real
    ]);
    let _ = my_data;
}
