import gleam/json
pub fn process(_value: json.Json) -> Nil { Nil }

pub fn main() {
  let _ = process(json.string("hello"))
  let _ = process(json.int(42))
  let _ = process(json.bool(True))
}
