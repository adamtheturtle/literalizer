defmodule Check do
  def f(_value), do: nil
  def x do
    f([1, 2])
  end
end
