defmodule Check do
  def f(_ops), do: nil
  def x do
    f([["DEL", "b", "10"], ["ADD", "a", "x"]])  # note
  end
end
