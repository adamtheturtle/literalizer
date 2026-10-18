pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("minimum", GInt(-2147483648)),
    #("below", GInt(-3000000000)),
  ])
  let _ = my_data
}
