import gleam/json

pub fn main() {
  let arena: json.Json = json.object([
    #("a", json.int(1)),
  ])
  let _ = arena
}
