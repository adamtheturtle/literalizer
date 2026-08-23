defmodule Check do
  def self(_value), do: nil
  def x do
    self("hello")
  end
end
