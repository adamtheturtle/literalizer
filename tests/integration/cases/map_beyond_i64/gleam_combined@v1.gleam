pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a", GInt(9223372036854775807)),
    #("b", GInt(9223372036854775808)),
  ])
  let my_data = GDict([
    #("a", GInt(9223372036854775807)),
    #("b", GInt(9223372036854775808)),
  ])
  let _ = my_data
}
