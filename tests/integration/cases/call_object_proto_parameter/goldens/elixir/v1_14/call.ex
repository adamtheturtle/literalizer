defmodule Check do
  def capture(__proto__), do: nil
  def x do
    capture(1)
  end
end
