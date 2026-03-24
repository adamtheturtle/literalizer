use std::collections::HashMap;
fn main() {
    {
        let my_data = HashMap::from([
            ("key", "it's here"),  // a comment
        ]);
        let _ = my_data;
    }
    let my_data;
    my_data = HashMap::from([
        ("key", "it's here"),  // a comment
    ]);
    let _ = my_data;
}
