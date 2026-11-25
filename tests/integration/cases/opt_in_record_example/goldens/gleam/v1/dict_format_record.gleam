pub type GVal0 {
  GVal0(name: String, active: Bool, scores: List(Int))
}

pub fn main() {
  let my_data = GVal0(
    name: "Ada",
    active: True,
    scores: [
      1,
      2,
      3,
    ],
  )
  let _ = my_data
}
