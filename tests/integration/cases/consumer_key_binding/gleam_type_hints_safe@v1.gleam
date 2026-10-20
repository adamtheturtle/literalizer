pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let key_binding = GDict([
    #("a", GInt(1)),
  ])
  let _ = key_binding
}
