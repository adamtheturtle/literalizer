defmodule Playlist do
  def new(_x), do: nil
end
defmodule Check do
  def x do
    Playlist.new(1)
    Playlist.new(2)
  end
end
