defmodule Playlist do
  def new(), do: nil
end
defmodule Check do
  def x do
    p = Playlist.new()
    _ = p
  end
end
