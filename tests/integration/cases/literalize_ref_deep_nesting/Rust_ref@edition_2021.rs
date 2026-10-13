use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    let deep = vec![
        vec![
            "one",
            "two",
        ],
        vec![
            "three",
            "four",
        ],
    ];
    let my_data = HashMap::from([
        ("a", HashMap::from([
            ("b", HashMap::from([
                ("c", deep),
            ])),
        ])),
    ]);
    let _ = &my_data;
}
