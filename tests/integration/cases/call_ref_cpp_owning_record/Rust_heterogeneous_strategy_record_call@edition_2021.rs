struct Record0 {
    value: &'static str,
}
fn main() {
    fn consume<A>(_value: A) {}
    let item = Record0 {
        value: "owned",
    };
    consume(item);
}
