import gleam/json

pub fn main() {
  let my_data: json.Json = json.object([
    #("date", json.string("0099-05-27")),
    #("naive", json.string("0001-01-01T12:30:00")),
    #("recent", json.string("2024-05-27T10:00:00")),
  ])
  let _ = my_data
}
