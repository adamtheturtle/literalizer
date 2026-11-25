pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}
pub fn thing_go(_before: a, _populated: b, _after: c) -> Nil { Nil }

pub fn main() {
  let _ = thing_go(#(), #(GInt(1)), #())
  let _ = thing_go(#(GStr("text")), #(GInt(2)), #())
  let _ = thing_go(#(), #(GStr("text")), #())
  let _ = thing_go(#(GStr("text")), #(GInt(2)), #(GInt(3)))
}
