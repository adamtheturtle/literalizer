
begin
    my_data = %q|
first line
  indented

last line
|
    raise "changed multiline string" unless my_data == "\nfirst line\n  indented\n\nlast line\n"
end
