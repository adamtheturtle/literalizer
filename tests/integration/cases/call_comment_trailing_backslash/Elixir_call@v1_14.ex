defmodule Check do
  def process(_value), do: nil
  def x do
    process(1)  # trail \ .
    process(2)  # second
  end
end
