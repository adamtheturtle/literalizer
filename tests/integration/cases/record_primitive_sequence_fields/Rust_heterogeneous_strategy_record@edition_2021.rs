#[derive(Clone)]
pub struct Record0 {
    pub flags: Vec<bool>,
    pub values: Vec<f64>,
    pub ints: Vec<i32>,
    pub text: Vec<&'static str>,
    pub nested_flags: Vec<Vec<bool>>,
    pub nested_values: Vec<Vec<f64>>,
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
    let _ = &my_data;
}
