// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    struct ObjType_;
    impl ObjType_ { fn ZVal<A>(&self, _value: A) {} }
    let obj = ObjType_;
    obj.ZVal(serde_json::json!(1));
}
