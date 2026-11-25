#[derive(Clone)]
pub struct Record0 {
    pub pair: (i32, i32),
    pub mixed: (i32, &'static str),
    pub triple: (i32, &'static str, bool),
    pub nested: ((i32, &'static str), (i32, bool, f64)),
    pub empty: (),
    pub single: (i32,),
    pub long: (i32, i32, i32, i32),
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
    let _ = &my_data;
}
