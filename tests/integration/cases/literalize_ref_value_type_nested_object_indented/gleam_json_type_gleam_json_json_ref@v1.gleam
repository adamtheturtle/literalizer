import gleam/json

pub fn main() {
      let shared: json.Json = json.preprocessed_array([
        json.int(1),
        json.int(2),
      ])
      let my_data: json.Json = json.object([
        #("field", json.object([#("nested", shared)])),
        #("text", json.string("first\n{ \" // }")),
      ])
  let _ = my_data
}
