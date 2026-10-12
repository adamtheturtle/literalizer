#[derive(Clone)]
struct Record0 {
    flags: (bool, bool),
    values: (f64, f64),
    ints: (i32, i32),
    text: (&'static str,),
    nested_flags: ((bool,), (bool,)),
    nested_values: ((f64,), (f64,)),
}
fn main() {
    let my_data = Record0 {
        flags: (
            true,
            false,
        ),
        values: (
            1.5,
            -2.25,
        ),
        ints: (
            1,
            2,
        ),
        text: (
            "a",
        ),
        nested_flags: (
            (
                true,
            ),
            (
                false,
            ),
        ),
        nested_values: (
            (
                1.5,
            ),
            (
                2.25,
            ),
        ),
    };
    let _ = my_data;
}
