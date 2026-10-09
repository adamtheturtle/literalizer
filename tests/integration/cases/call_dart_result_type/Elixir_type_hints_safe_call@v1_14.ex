defmodule Check do
  def make_widget(_count), do: nil
  def x do
    my_data = make_widget(42)
    _ = my_data
  end
end
