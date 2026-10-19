import gleam/bit_array as literalizer_bit_array
pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("fffe", GStr({ let assert Ok(literalizer_decoded) = literalizer_bit_array.to_string(<<239, 191, 190>>) literalizer_decoded })),
    #("ffff", GStr({ let assert Ok(literalizer_decoded) = literalizer_bit_array.to_string(<<239, 191, 191>>) literalizer_decoded })),
  ])
  let _ = my_data
}
