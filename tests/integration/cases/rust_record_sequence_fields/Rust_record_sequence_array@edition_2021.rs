struct Record0 {
    short: [i32; 1],
    long: [i32; 2],
}
fn main() {
    let my_data = Record0 {
        short: [
            1,
        ],
        long: [
            1,
            2,
        ],
    };
    let _ = my_data;
}
