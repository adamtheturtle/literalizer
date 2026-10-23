defmodule Check do
  def process(_value), do: nil
  def x do
    process(nil)
    process([1, 2])
  end
end
