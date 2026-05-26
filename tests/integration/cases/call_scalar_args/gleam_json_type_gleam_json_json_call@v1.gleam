import gleam/json
pub fn process(_value: json.Json) -> Nil { Nil }

pub fn main() {
  process(json.string("hello"))
  process(json.int(42))
  process(json.bool(True))
}
