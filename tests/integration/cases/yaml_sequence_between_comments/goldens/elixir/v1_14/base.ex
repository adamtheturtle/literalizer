defmodule Check do
  def x do
    my_data = [
        %{"item" => "existing"},
        # This comment describes the next item.
        %{"item" => "next"},
    ]
    _ = my_data
  end
end
