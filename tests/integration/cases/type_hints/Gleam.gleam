import gleam/dict

pub fn main() {
  let my_data = dict.from_list([
    #("name", "Alice"),
    #("age", 30),
    #("active", True),
    #("score", Nil),
    #("joined", "2024-01-15"),
    #("last_login", "2024-01-15T12:30:00+00:00"),
    #("avatar", "48656c6c6f"),
  ])
  let _ = my_data
}
