pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a_b", GInt(0b1)),
    #("a-b", GInt(0b10)),
    #("averyveryverylongkeynamethatgoesonandonandon", GInt(0b11)),
    #("averyveryverylongkeynamethatgoesonandmore", GInt(0b100)),
  ])
  let _ = my_data
}
