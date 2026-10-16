import gleam/json
pub fn thing_go(_value: json.Json) -> Nil { Nil }

pub fn main() {
  let my_data: json.Json = thing_go(json.preprocessed_array([]))
  let _ = my_data
}
