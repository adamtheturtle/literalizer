
{
  const my_data = `
first line
  indented

last line
`;
    if (my_data !== "\nfirst line\n  indented\n\nlast line\n") { throw new Error("changed multiline string"); }
}
