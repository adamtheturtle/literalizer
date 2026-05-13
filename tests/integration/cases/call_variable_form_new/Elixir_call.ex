defmodule Check do
  def x do
    def make_widget(_count), do: nil
    result = make_widget(42)
    _ = result
  end
end
