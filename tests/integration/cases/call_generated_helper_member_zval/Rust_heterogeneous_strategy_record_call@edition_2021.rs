// Preserve intentional caller identifier spelling.
#![allow(non_snake_case)]
fn main() {
    struct ObjType;
    impl ObjType { fn ZVal<A>(&self, _value: A) {} }
    let obj = ObjType;
    obj.ZVal(1);
}
