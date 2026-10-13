#[allow(non_snake_case)]
fn main() {
    fn process<A>(_value: A) {}
    process(None::<()>);
    process("hello");
}
