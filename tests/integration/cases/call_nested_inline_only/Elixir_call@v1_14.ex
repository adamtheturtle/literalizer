defmodule Check do
  def f(_a, _b), do: nil
  def x do
    f(2, "hello")  # trailing note
    f(3, "world")  # another note
  end
end
