struct Record0 {
    short: (i32,),
    long: (i32, i32),
}
fn main() {
    let my_data = Record0 {
        short: (
            1,
        ),
        long: (
            1,
            2,
        ),
    };
    let _ = my_data;
}
