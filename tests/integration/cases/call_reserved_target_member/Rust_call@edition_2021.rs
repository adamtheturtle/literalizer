fn main() {
    struct ObjType_;
    impl ObjType_ { fn class<A>(&self, _a: A) {} }
    let obj = ObjType_;
    obj.class(42);
}
