pub type GVal {
  GStr(String)
  GList(List(GVal))
}
pub fn op(_value: a) -> Nil { Nil }

pub fn main() {
  let _ = op(GStr("hello"))
}
