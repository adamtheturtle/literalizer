#[derive(Clone)]
pub struct Record0 {
    pub numbers: Vec<i32>,
    pub nested_numbers: Vec<Vec<i32>>,
    pub words: Vec<&'static str>,
    pub flag: bool,
}
fn main() {
    let my_data = Record0 {
        numbers: vec![
            1,
            2,
        ],
        nested_numbers: vec![
            vec![
                3,
                4,
            ],
            vec![
                5,
                6,
            ],
        ],
        words: vec![
            "s",
        ],
        flag: true,
    };
    let _ = &my_data;
}
