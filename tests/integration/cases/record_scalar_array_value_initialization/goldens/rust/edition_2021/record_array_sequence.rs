#[derive(Clone)]
pub struct Record0 {
    pub numbers: [i32; 2],
    pub nested_numbers: [[i32; 2]; 2],
    pub words: [&'static str; 1],
    pub flag: bool,
}
fn main() {
    let my_data = Record0 {
        numbers: [
            1,
            2,
        ],
        nested_numbers: [
            [
                3,
                4,
            ],
            [
                5,
                6,
            ],
        ],
        words: [
            "s",
        ],
        flag: true,
    };
    let _ = &my_data;
}
