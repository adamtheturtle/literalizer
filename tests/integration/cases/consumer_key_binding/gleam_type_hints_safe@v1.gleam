pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let k = GDict([
    #("a", GInt(1)),
  ])
  let _ = k
}
