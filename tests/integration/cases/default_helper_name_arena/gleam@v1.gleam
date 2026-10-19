pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let arena = GDict([
    #("a", GInt(1)),
  ])
  let _ = arena
}
