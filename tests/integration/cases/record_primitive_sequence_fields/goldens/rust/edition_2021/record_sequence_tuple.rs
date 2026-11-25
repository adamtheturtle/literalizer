#[derive(Clone)]
pub struct Record0 {
    pub flags: (bool, bool),
    pub values: (f64, f64),
    pub ints: (i32, i32),
    pub text: (&'static str,),
    pub nested_flags: ((bool,), (bool,)),
    pub nested_values: ((f64,), (f64,)),
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
    let _ = &my_data;
}
