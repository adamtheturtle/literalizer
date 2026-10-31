#[derive(Clone)]
pub struct Record0 {
    pub name: &'static str,
    pub values: Vec<i32>,
}
fn main() {
    fn consume<A>(_value: A) {}
    let item = Record0 {
        name: "first",
        values: vec![
            1,
            2,
        ],
    };
    consume(item.clone());
}
