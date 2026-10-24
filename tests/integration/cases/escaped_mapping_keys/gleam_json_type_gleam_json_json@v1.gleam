import gleam/json

pub fn main() {
  let my_data: json.Json = json.object([
    #("quote\"backslash\\", json.int(1)),
    #("line\nbreak", json.int(2)),
    #("$(literal)${text}", json.int(3)),
    #("RStr prefix", json.int(4)),
  ])
  let _ = my_data
}
