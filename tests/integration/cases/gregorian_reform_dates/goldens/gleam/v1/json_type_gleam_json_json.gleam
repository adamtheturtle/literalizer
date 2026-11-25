import gleam/json

pub fn main() {
  let my_data: json.Json = json.object([
    #("ancient_date", json.string("1500-03-01")),
    #("modern_date", json.string("2024-01-15")),
    #("before_date", json.string("1582-10-04")),
    #("gap_date", json.string("1582-10-10")),
    #("transition_date", json.string("1582-10-15")),
    #("after_date", json.string("1582-10-16")),
    #("before_naive", json.string("1582-10-04T12:30:00.000001")),
    #("gap_naive", json.string("1582-10-10T12:30:00.500000")),
    #("transition_positive", json.string("1582-10-15T00:30:00+18:00")),
    #("transition_negative", json.string("1582-10-15T23:30:00-18:00")),
    #("after_positive", json.string("1582-10-16T00:30:00+18:00")),
  ])
  let _ = my_data
}
