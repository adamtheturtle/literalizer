pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("lower", GInt(3735928559)),
    #("upper", GInt(31)),
    #("negative", GInt(-16)),
    #("zero", GInt(0)),
  ])
  let _ = my_data
}
