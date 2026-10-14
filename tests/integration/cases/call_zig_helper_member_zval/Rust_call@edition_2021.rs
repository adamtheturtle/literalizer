fn main() {
    struct ObjType;
    impl ObjType { fn ZVal<A>(&self, _value: A) {} }
    let obj = ObjType;
    obj.ZVal(1);
}
