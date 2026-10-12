defmodule Check do
  def make_widget(_count), do: nil
  def x do
    my_data = 42
    my_data = make_widget(my_data) // note
    make_widget(my_data)
  end
end
