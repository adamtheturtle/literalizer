struct Record0 {
    numbers: [i32; 1],
    words: [&'static str; 1],
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
    let _ = my_data;
}
