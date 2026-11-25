defmodule Check do
  def class(_a), do: nil
  def x do
    class(42)
  end
end
