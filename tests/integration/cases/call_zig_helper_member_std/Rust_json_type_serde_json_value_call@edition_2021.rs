// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    struct ObjType_;
    impl ObjType_ { fn std<A>(&self, _value: A) {} }
    let obj = ObjType_;
    obj.std(serde_json::json!(1));
}
