defmodule Check do
  def f(_a), do: nil
  def repr(_arg), do: nil
  def x do
    ref_data = 1
    repr(f(ref_data))
  end
end
