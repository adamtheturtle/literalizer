import gleam/json

pub fn main() {
  let shared: json.Json = json.preprocessed_array([
    json.int(1),
    json.int(2),
  ])
  let build: json.Json = json.preprocessed_array([
    json.int(1),
    json.int(2),
  ])
  let json_object: json.Json = json.preprocessed_array([
    json.int(1),
    json.int(2),
  ])
  let json_allocator: json.Json = json.preprocessed_array([
    json.int(1),
    json.int(2),
  ])
  let json_entries: json.Json = json.preprocessed_array([
    json.int(1),
    json.int(2),
  ])
  let json_entry: json.Json = json.preprocessed_array([
    json.int(1),
    json.int(2),
  ])
  let my_data: json.Json = json.object([
    #("field", shared),
    #("nested", json.preprocessed_array([shared, json.object([])])),
    #("build", build),
    #("json_object", json_object),
    #("json_allocator", json_allocator),
    #("json_entries", json_entries),
    #("json_entry", json_entry),
  ])
  let _ = my_data
}
