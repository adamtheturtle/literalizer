pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a", GInt(9_223_372_036_854_775_807)),
    #("b", GInt(9_223_372_036_854_775_808)),
  ])
  let _ = my_data
}
