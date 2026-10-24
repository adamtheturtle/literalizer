use std::collections::HashMap;
fn main() {
    let my_data = [
        HashMap::from([("values", [] as [String; 0])]),
        <HashMap<&str, [String; 0]>>::from([]),
    ];
    let _ = &my_data;
}
