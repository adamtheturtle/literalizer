defmodule Check do
  def make_widget(_count), do: nil
  def x do
    my_data = make_widget(42)
    my_data = make_widget(42) // note
  end
end
