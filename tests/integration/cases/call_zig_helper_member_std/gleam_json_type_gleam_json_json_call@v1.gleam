import gleam/json
pub fn obj_std(_value: json.Json) -> Nil { Nil }

pub fn main() {
  obj_std(json.int(1))
}
