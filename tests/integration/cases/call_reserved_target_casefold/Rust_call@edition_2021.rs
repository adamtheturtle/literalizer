// Preserve intentional caller identifier spelling.
#![allow(non_snake_case)]
fn main() {
    fn BEGIN<A>(_a: A) {}
    BEGIN(42);
}
