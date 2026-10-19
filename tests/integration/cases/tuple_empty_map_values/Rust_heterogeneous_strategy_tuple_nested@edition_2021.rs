#[derive(Clone)]
pub struct Record0 {
    pub filled: (i32, &'static str),
    pub empty: Vec<String>,
}
fn main() {
    let my_data = Record0 {
        filled: (
            1,
            "value",
        ),
        empty: Vec::<String>::new(),
    };
    let _ = &my_data;
}
