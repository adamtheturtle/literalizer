defmodule Check do
  def f(_a), do: nil
  def x do
    ref_data = 1
    f(ref_data)
  end
end
