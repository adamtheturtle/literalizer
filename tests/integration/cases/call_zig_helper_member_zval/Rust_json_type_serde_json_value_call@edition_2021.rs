// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    struct ObjType;
    impl ObjType { fn ZVal<A>(&self, _value: A) {} }
    let obj = ObjType;
    obj.ZVal(serde_json::json!(1));
}
