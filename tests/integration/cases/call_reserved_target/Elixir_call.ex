defmodule Check do
  def op(_value), do: nil
  def x do
    op("hello")
  end
end
