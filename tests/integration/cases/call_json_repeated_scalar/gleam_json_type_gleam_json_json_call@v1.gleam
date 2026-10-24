import gleam/json
pub fn consume(_value: json.Json) -> Nil { Nil }

pub fn main() {
  let shared: json.Json = json.int(42)
  let _ = consume(json.preprocessed_array([shared, shared]))
}
