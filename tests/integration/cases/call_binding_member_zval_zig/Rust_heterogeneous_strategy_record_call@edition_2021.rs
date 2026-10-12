fn main() {
    struct ObjType_;
    impl ObjType_ { fn ZVal<A>(&self, __arg: A) {} }
    let obj = ObjType_;
    let my_data = obj.ZVal(42) // note;
    let _ = my_data;
}
