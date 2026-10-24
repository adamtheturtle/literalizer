import gleam/json
pub fn consume(_value: json.Json) -> Nil { Nil }

pub fn main() {
  let shared: json.Json = json.preprocessed_array([
    json.int(1),
    json.int(2),
  ])
  let _ = consume(json.preprocessed_array([shared, shared]))
}
