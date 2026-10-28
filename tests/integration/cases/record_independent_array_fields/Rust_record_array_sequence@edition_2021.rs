#[derive(Clone)]
pub struct Record0 {
    pub numbers: [i32; 1],
    pub words: [&'static str; 1],
}
fn main() {
    let my_data = Record0 {
        numbers: [
            1,
        ],
        words: [
            "s",
        ],
    };
    let _ = &my_data;
}
