fn main() {
    struct ObjType;
    impl ObjType { fn ZKV<A>(&self, _value: A) {} }
    let obj = ObjType;
    obj.ZKV(1);
}
