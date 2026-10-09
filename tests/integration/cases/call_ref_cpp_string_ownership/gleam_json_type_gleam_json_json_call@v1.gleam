import gleam/json
pub fn consume(_value: json.Json) -> Nil { Nil }

pub fn main() {
  let item: json.Json = json.string("s")
  consume(item)
}
