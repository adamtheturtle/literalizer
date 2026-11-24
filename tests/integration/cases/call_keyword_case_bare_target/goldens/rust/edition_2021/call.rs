// Preserve intentional caller identifier spelling.
#![allow(non_snake_case)]
fn main() {
    fn Before<A>(_value: A) {}
    Before(1);
}
