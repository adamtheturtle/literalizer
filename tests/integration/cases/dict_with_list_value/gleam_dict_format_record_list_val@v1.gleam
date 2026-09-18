pub type GVal0 {
  GVal0(name: String, scores: List(Int))
}

pub fn main() {
  let my_data = GVal0(
    name: "Alice",
    scores: [
      10,
      20,
      30,
    ],
  )
  let _ = my_data
}
