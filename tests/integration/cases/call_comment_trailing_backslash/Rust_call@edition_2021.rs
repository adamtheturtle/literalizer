#[allow(non_snake_case)]
fn main() {
    fn process<A>(_value: A) {}
    process(1);  // trail \ .
    process(2);  // second
}
