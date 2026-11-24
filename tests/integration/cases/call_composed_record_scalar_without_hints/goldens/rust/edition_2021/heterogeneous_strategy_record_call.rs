#[derive(Clone)]
pub struct Record0 {
    pub a: i32,
}
fn main() {
    fn consume<A>(_value: A) {}
    let item = Record0 {
        a: 1,
    };
    consume(item.clone());
}
