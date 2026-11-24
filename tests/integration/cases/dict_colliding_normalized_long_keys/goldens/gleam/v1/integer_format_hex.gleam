pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a_b", GInt(0x1)),
    #("a-b", GInt(0x2)),
    #("averyveryverylongkeynamethatgoesonandonandon", GInt(0x3)),
    #("averyveryverylongkeynamethatgoesonandmore", GInt(0x4)),
  ])
  let _ = my_data
}
