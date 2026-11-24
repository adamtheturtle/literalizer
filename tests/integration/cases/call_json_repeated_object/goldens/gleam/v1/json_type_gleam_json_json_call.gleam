import gleam/json
pub fn consume(_value: json.Json) -> Nil { Nil }

pub fn main() {
  let shared: json.Json = json.object([
    #("value", json.preprocessed_array([json.int(1), json.int(2)])),
  ])
  let _ = consume(json.object([#("left", shared), #("right", shared)]))
}
