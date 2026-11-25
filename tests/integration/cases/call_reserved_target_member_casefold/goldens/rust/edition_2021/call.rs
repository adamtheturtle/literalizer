// Preserve intentional caller identifier spelling.
#![allow(non_snake_case)]
fn main() {
    struct ObjType;
    impl ObjType { fn BEGIN<A>(&self, _a: A) {} }
    let obj = ObjType;
    obj.BEGIN(42);
}
