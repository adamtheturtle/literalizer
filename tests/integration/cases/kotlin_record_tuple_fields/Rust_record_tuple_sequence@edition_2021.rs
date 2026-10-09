struct Record0 {
    pair: (i32, i32),
    mixed: (i32, &'static str),
    triple: (i32, &'static str, bool),
    nested: ((i32, &'static str), (i32, bool, f64)),
    empty: (),
    single: (i32,),
    long: (i32, i32, i32, i32),
}
fn main() {
    let my_data = Record0 {
        pair: (
            1,
            2,
        ),
        mixed: (
            1,
            "text",
        ),
        triple: (
            1,
            "text",
            true,
        ),
        nested: (
            (
                1,
                "text",
            ),
            (
                2,
                false,
                3.5,
            ),
        ),
        empty: (),
        single: (
            1,
        ),
        long: (
            1,
            2,
            3,
            4,
        ),
    };
    let _ = my_data;
}
