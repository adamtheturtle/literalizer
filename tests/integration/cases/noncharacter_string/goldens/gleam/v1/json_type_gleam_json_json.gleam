import gleam/json
import gleam/bit_array

pub fn main() {
  let my_data: json.Json = json.object([
    #("fffe", json.string({ let assert Ok(decoded) = bit_array.to_string(<<239, 191, 190>>) decoded })),
    #("ffff", json.string({ let assert Ok(decoded) = bit_array.to_string(<<239, 191, 191>>) decoded })),
  ])
  let _ = my_data
}
