fn main() {
    struct ObjType_;
    impl ObjType_ { fn ZKV<A>(&self, _value: A) {} }
    let obj = ObjType_;
    obj.ZKV(1);
}
