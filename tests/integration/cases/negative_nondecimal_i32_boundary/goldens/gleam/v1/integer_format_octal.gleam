pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("minimum", GInt(-{0o20000000000})),
    #("below", GInt(-{0o26264057000})),
  ])
  let _ = my_data
}
