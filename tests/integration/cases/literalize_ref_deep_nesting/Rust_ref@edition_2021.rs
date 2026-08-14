use std::collections::HashMap;
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
    let _ = my_data;
}
