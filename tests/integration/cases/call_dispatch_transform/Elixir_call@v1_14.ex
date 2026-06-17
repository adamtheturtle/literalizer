defmodule Check do
  def record(_value), do: nil
  def flush(_count), do: nil
  def x do
    record(42)
    flush(3)
  end
end
