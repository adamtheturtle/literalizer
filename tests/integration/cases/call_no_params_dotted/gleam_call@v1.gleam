pub type GVal {
  GList(List(GVal))
}
pub fn throttler_check() -> Nil { Nil }

pub fn main() {
  let _ = throttler_check()
  let _ = throttler_check()
}
