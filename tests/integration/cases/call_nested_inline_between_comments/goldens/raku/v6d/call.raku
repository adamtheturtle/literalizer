sub f(*@a, *%kw) {}
f(2, 'hello');  # trailing note
# next element
f(3, 'world');
