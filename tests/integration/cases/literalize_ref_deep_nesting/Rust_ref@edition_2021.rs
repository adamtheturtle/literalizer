use std::collections::HashMap;
fn main() {
    let deep = vec![
        vec![
            1,
            2,
        ],
        vec![
            3,
            4,
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
