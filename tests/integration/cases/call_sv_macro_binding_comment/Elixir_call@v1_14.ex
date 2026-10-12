defmodule Check do
  def make_widget(_count), do: nil
  def x do
    my_data = (`__LINE__ > 0) ? make_widget(42) : make_widget(42) // trailing `marker
    _ = my_data
  end
end
