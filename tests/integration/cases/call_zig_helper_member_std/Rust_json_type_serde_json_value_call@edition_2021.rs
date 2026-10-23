// Permit serde_json::json! to expand wide values.
#![recursion_limit = "4096"]
fn main() {
    struct ObjType;
    impl ObjType { fn std<A>(&self, _value: A) {} }
    let obj = ObjType;
    obj.std(serde_json::json!(1));
}
