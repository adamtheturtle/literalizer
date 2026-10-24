import gleam/json

pub fn main() {
  let my_data: json.Json = json.object([
    #("__proto__", json.object([#("x", json.int(1))])),
    #("n", json.object([#("__proto__", json.int(3))])),
    #("y", json.int(2)),
  ])
  let _ = my_data
}
