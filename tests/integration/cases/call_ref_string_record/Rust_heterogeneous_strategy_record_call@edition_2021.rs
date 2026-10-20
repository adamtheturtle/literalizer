#[derive(Clone)]
pub struct Record0 {
    pub value: &'static str,
}
fn main() {
    fn consume<A>(_value: A) {}
    let item = Record0 {
        value: "owned",
    };
    consume(item);
}
