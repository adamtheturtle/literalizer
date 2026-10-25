import gleam/json

pub fn main() {
  let ref_data: json.Json = json.preprocessed_array([
    json.int(1),
    json.int(2),
  ])
  let my_data: json.Json = ref_data
  let _ = my_data
}
