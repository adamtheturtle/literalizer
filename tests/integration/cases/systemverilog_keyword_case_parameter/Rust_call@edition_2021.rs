// Preserve intentional caller identifier spelling.
#![allow(non_snake_case)]
fn main() {
    fn make_widget<A>(_Before: A) {}
    make_widget(1);
}
