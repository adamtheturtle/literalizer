defmodule Check do
  def f(_a), do: nil
  def x do
    # scalar heading
    # second heading line
    # scalar inline
    # inline continuation
    # scalar trailing
    f(42)
  end
end
