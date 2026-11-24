#[derive(Clone)]
pub struct Record0 {
    pub flags: [bool; 2],
    pub values: [f64; 2],
    pub ints: [i32; 2],
    pub text: [&'static str; 1],
    pub nested_flags: [[bool; 1]; 2],
    pub nested_values: [[f64; 1]; 2],
}
fn main() {
    let my_data = Record0 {
        flags: [
            true,
            false,
        ],
        values: [
            1.5,
            -2.25,
        ],
        ints: [
            1,
            2,
        ],
        text: [
            "a",
        ],
        nested_flags: [
            [
                true,
            ],
            [
                false,
            ],
        ],
        nested_values: [
            [
                1.5,
            ],
            [
                2.25,
            ],
        ],
    };
    let _ = &my_data;
}
