struct Record0 {
    numbers: [i32; 2],
    nested_numbers: [[i32; 2]; 2],
    words: [&'static str; 1],
    flag: bool,
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
    let _ = my_data;
}
