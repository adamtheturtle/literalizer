import gleam/json
pub fn thing_go(_before: json.Json, _populated: json.Json, _after: json.Json) -> Nil { Nil }

pub fn main() {
  let _ = thing_go(json.preprocessed_array([]), json.preprocessed_array([json.int(1)]), json.preprocessed_array([]))
  let _ = thing_go(json.preprocessed_array([json.string("text")]), json.preprocessed_array([json.int(2)]), json.preprocessed_array([]))
  let _ = thing_go(json.preprocessed_array([]), json.preprocessed_array([json.string("text")]), json.preprocessed_array([]))
  let _ = thing_go(json.preprocessed_array([json.string("text")]), json.preprocessed_array([json.int(2)]), json.preprocessed_array([json.int(3)]))
}
