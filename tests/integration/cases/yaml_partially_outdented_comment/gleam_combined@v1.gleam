pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a", GDict([
      #("b", GList([GInt(1)])),
      // Outdented from the sequence, so the inner mapping claims this.
      #("c", GInt(2)),
    ])),
    // Outdented from the inner mapping too, so the root claims this.
    #("d", GInt(3)),
  ])
  let my_data = GDict([
    #("a", GDict([
      #("b", GList([GInt(1)])),
      // Outdented from the sequence, so the inner mapping claims this.
      #("c", GInt(2)),
    ])),
    // Outdented from the inner mapping too, so the root claims this.
    #("d", GInt(3)),
  ])
  let _ = my_data
}
