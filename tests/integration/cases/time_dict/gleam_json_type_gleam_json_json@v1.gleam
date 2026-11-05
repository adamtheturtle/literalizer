import gleam/json

pub fn main() {
  let my_data: json.Json = json.object([
    #("morning", json.string("09:30:00")),
    #("afternoon", json.string("14:15:00")),
    #("evening", json.string("23:59:59")),
  ])
  let _ = my_data
}
