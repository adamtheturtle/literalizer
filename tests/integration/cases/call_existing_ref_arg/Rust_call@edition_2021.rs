#[allow(non_snake_case)]
fn main() {
    fn process<A>(_value: A) {}
    let existing = 42;
    process(existing);
}
