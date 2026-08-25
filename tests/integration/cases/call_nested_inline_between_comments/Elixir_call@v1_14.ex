defmodule Check do
  def f(_a, _b), do: nil
  def x do
    f(2, "hello")  # trailing note
    # next element
    f(3, "world")
  end
end
