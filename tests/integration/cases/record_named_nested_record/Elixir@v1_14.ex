defmodule Check do
  def x do
    my_data = %{
        "project" => "alpha",
        "lead_item" => %{"id" => 100, "label" => "first item", "enabled" => false, "related_ids" => [102, 103]},
    }
    _ = my_data
  end
end
