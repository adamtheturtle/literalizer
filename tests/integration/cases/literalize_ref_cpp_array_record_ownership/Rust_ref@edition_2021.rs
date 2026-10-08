struct Record1 {
    values: [i32; 2],
}
struct Record2 {
    nested: [[i32; 2]; 2],
}
struct Record0 {
    trivial: Record1,
    nested: Record2,
}
fn main() {
    let trivial = Record1 {
        values: [
            1,
            2,
        ],
    };
    let nested = Record2 {
        nested: [
            [
                1,
                2,
            ],
            [
                3,
                4,
            ],
        ],
    };
    let my_data = HashMap::from([
        ("trivial", trivial),
        ("nested", nested),
    ]);
    let _ = my_data;
}
