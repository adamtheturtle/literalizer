defmodule Check do
  def process(_value), do: nil
  def x do
    process(1)  # note<U+2028>still commented<U+2029>done
  end
end
