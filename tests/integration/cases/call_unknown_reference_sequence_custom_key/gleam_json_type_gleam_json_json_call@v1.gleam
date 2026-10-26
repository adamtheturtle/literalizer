import gleam/json
pub fn process(_data: json.Json) -> Nil { Nil }

pub fn main() {
  let untyped_value: json.Json = json.preprocessed_array([])
  let _ = process(json.preprocessed_array([untyped_value, untyped_value]))
}
