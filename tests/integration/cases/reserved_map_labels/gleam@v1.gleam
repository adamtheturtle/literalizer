pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("if", GInt(1)),
    #("then", GInt(2)),
    #("else", GInt(3)),
    #("let", GInt(4)),
    #("in", GInt(5)),
    #("using", GInt(6)),
    #("missing", GInt(7)),
    #("assert", GInt(8)),
    #("as", GInt(9)),
    #("Infinity", GInt(10)),
    #("NaN", GInt(11)),
    #("merge", GInt(12)),
    #("Some", GInt(13)),
    #("toMap", GInt(14)),
    #("forall", GInt(15)),
    #("with", GInt(16)),
    #("ordinary", GInt(17)),
  ])
  let _ = my_data
}
