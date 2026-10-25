import gleam/json
pub fn process(_data: json.Json) -> Nil { Nil }

pub fn main() {
  let unknown_value: json.Json = json.preprocessed_array([])
  let _ = process(json.preprocessed_array([unknown_value]))
}
