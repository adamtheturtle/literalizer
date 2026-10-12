defmodule Check do
  def make_widget(_count), do: nil
  def x do
    my_data = ("\"prefix ${"// payload"}\"").length >= 0 ? make_widget(42) : make_widget(42)
    _ = my_data
  end
end
