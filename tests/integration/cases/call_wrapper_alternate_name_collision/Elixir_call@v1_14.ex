defmodule Check do
  def check_wrapper(_a), do: nil
  def x do
    check_wrapper(42)
  end
end
