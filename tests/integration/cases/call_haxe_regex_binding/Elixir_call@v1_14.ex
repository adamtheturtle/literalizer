defmodule Check do
  def make_widget(_count), do: nil
  def x do
    my_data = (~/\//).match("/") ? make_widget(42) : null
    _ = my_data
  end
end
