import gleam/json

pub fn main() {
  let my_data: json.Json = json.object([
    #("v", json.string("a﻿b")),
  ])
  let _ = my_data
}
