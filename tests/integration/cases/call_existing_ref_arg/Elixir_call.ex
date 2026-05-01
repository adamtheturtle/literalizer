defmodule Check do
  def process(_value), do: nil
  def x do
    existing = 42
    process(existing)
  end
end
