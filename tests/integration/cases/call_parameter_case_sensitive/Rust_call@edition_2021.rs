// Preserve intentional caller identifier spelling.
#![allow(non_snake_case)]
fn main() {
    fn process<A>(_IF: A) {}
    process(42);
}
