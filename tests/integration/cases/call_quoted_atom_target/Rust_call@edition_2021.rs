// Preserve intentional caller identifier spelling.
#![allow(non_snake_case)]
fn main() {
    fn DoThing<A>(_x: A) {}
    DoThing(1);
    DoThing(2);
}
