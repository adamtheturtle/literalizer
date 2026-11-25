fn main() {
    struct ObjType;
    impl ObjType { fn class<A>(&self, _a: A) {} }
    let obj = ObjType;
    obj.class(42);
}
