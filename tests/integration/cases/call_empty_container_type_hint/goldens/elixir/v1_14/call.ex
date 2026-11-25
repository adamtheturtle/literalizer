defmodule Check do
  def process(_values, _count), do: nil
  def x do
    process([1, %{}], 42)
  end
end
