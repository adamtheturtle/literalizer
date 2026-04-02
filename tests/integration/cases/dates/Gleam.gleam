import gleam/dict

pub fn main() {
  let my_data = dict.from_list([
    #("date", "2024-01-15"),
    #("datetime", "2024-01-15T12:30:00+00:00"),
  ])
  let _ = my_data
}
