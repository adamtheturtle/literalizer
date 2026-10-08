use std::collections::HashMap;
fn main() {
        let shared = vec![
            1,
            2,
        ];
        let my_data = HashMap::from([
            ("a", shared),
        ]);
    let _ = my_data;
}
