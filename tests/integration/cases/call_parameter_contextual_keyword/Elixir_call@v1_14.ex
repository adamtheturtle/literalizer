defmodule Check do
  def f(_using), do: nil
  def x do
    f(1)
  end
end
