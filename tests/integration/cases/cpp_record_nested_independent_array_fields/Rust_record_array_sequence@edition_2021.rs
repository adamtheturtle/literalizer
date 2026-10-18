#[derive(Clone)]
pub struct Record0 {
    pub numbers: [[i32; 1]; 2],
    pub words: [[&'static str; 1]; 2],
}
fn main() {
    let my_data = Record0 {
        numbers: [
            [
                1,
            ],
            [
                2,
            ],
        ],
        words: [
            [
                "s",
            ],
            [
                "t",
            ],
        ],
    };
    let _ = &my_data;
}
