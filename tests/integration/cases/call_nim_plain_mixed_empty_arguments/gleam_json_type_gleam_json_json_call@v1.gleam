import gleam/json
pub fn make_widget(_before: json.Json, _populated: json.Json, _after: json.Json) -> Nil { Nil }

pub fn main() {
  let _ = make_widget(json.preprocessed_array([]), json.preprocessed_array([json.int(1)]), json.preprocessed_array([]))
  let _ = make_widget(json.preprocessed_array([json.string("text")]), json.preprocessed_array([json.int(2)]), json.preprocessed_array([]))
  let _ = make_widget(json.preprocessed_array([]), json.preprocessed_array([json.string("text")]), json.preprocessed_array([]))
  let _ = make_widget(json.preprocessed_array([json.string("text")]), json.preprocessed_array([json.int(2)]), json.preprocessed_array([json.int(3)]))
}
