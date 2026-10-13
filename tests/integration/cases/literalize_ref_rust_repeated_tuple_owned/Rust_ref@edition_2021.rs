use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    let shared = (
        vec![
            1,
            2,
        ],
        HashMap::from([
            ("value", 1),
        ]),
    );
    let my_data = vec![
        shared.clone(),
        shared.clone(),
    ];
    let _ = &my_data;
}
