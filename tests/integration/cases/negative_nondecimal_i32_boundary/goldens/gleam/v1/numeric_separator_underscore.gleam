pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("minimum", GInt(-2_147_483_648)),
    #("below", GInt(-3_000_000_000)),
  ])
  let _ = my_data
}
