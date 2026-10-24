pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let std = GDict([
    #("a", GInt(1)),
  ])
  let _ = std
}
