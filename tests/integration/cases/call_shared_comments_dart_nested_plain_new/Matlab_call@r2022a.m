make_widget = @(varargin) [];
my_data = ("${"${"// payload"}"}").length >= 0 ? make_widget(42) : make_widget(42);
