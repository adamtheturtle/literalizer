defmodule Check do
  def process(_xs), do: nil
  def x do
    process([
        1,
        2,
    ])
    process([
        3,
    ])
  end
end
