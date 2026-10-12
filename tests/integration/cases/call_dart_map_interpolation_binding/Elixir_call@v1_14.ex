defmodule Check do
  def make_widget(_count), do: nil
  def x do
    my_data = "${{'value': '// payload'}['value']}" // trailing
    // extra
    _ = my_data
  end
end
