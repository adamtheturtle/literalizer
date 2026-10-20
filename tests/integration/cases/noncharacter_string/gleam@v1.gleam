import gleam/bit_array
pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("fffe", GStr({ let assert Ok(decoded) = bit_array.to_string(<<239, 191, 190>>) decoded })),
    #("ffff", GStr({ let assert Ok(decoded) = bit_array.to_string(<<239, 191, 191>>) decoded })),
  ])
  let _ = my_data
}
