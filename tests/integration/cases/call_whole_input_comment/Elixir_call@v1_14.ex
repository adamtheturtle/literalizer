defmodule Check do
  def f(_a), do: nil
  def x do
    f([1])  # note
  end
end
