// Preserve intentional caller identifier spelling.
#![allow(non_snake_case)]
fn main() {
    struct ObjType;
    impl ObjType { fn ZVal<A>(&self, __arg: A) {} }
    let obj = ObjType;
    let my_data = obj.ZVal(42); // note
    let _ = &my_data;
}
