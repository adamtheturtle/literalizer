defmodule Check do
  def f(_a), do: nil
  def x do
    x = 1
    f(x)
  end
end
