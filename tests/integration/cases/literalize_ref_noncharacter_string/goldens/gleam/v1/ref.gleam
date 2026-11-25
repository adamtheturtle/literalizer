import gleam/bit_array
pub type GVal {
  GStr(String)
}

pub fn main() {
  let source_value = GStr({ let assert Ok(decoded) = bit_array.to_string(<<239, 191, 190, 239, 191, 191>>) decoded })
  let my_data = source_value
  let _ = my_data
}
