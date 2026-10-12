fn main() {
    struct ObjType_;
    impl ObjType_ { fn BEGIN<A>(&self, _a: A) {} }
    let obj = ObjType_;
    obj.BEGIN(42);
}
