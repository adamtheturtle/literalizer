defmodule Check do
  def make_widget(_value), do: nil
  def x do
    my_data = make_widget([])
    _ = my_data
  end
end
