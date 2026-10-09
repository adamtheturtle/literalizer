struct Record0 {
    numbers: [[i32; 1]; 2],
    words: [[&'static str; 1]; 2],
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
    let _ = my_data;
}
