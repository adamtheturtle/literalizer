defmodule Check do
  def record_entry(_s, _n, _b), do: nil
  def x do
    my_data = record_entry("a", 1, true)
    _ = my_data
  end
end
