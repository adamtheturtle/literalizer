make_widget = @(varargin) [];
consume = @(varargin) [];
my_data = make_widget(42, 3);
consume(3, my_data)
