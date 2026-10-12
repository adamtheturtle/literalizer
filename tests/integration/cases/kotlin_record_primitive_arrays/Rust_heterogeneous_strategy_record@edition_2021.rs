#[derive(Clone)]
struct Record0 {
    flags: Vec<bool>,
    values: Vec<f64>,
    ints: Vec<i32>,
    text: Vec<&'static str>,
    nested_flags: Vec<Vec<bool>>,
    nested_values: Vec<Vec<f64>>,
}
fn main() {
    let my_data = Record0 {
        flags: vec![
            true,
            false,
        ],
        values: vec![
            1.5,
            -2.25,
        ],
        ints: vec![
            1,
            2,
        ],
        text: vec![
            "a",
        ],
        nested_flags: vec![
            vec![
                true,
            ],
            vec![
                false,
            ],
        ],
        nested_values: vec![
            vec![
                1.5,
            ],
            vec![
                2.25,
            ],
        ],
    };
    let _ = my_data;
}
