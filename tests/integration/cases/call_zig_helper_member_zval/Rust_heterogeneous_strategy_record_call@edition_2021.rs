fn main() {
    struct ObjType_;
    impl ObjType_ { fn ZVal<A>(&self, _value: A) {} }
    let obj = ObjType_;
    obj.ZVal(1);
}
