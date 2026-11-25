defmodule Check do
  def x do
    my_data = %{
        "collection" => "alpha",
        "featured_entry" => %{"id" => 100, "label" => "first entry", "enabled" => false, "related_ids" => [102, 103]},
    }
    _ = my_data
  end
end
