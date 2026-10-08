struct Record0 {
    value: i32,
}
fn main() {
    fn consume<A>(_value: A) {}
    let item = Record0 {
        value: 1,
    };
    consume(item);
}
