import gleam/json

pub fn main() {
  let my_data: json.Json = json.object([
    #("exact_millisecond", json.string("09:30:15.123000")),
    #("sub_millisecond", json.string("09:30:15.123456")),
  ])
  let _ = my_data
}
