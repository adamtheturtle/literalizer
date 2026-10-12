defmodule Check do
  def make_widget(_count), do: nil
  def x do
    my_data = make_widget(42) ?
    make_widget(42) // inner
    : nil // trailing
    _ = my_data
  end
end
