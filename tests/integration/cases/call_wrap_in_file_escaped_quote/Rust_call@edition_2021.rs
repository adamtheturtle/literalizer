#[allow(non_snake_case)]
fn main() {
    fn process<A>(_v: A) {}
    process("a\"b");
}
