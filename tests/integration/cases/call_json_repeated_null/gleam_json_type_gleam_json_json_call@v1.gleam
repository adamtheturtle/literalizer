import gleam/json
pub fn consume(_value: json.Json) -> Nil { Nil }

pub fn main() {
  let shared: json.Json = json.null()
  let _ = consume(json.object([#("left", shared), #("nested", json.preprocessed_array([shared]))]))
}
