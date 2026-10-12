make_widget = @(varargin) [];
my_data = ($"{{payload}} {1://}").Length >= 0 ? make_widget(42) : make_widget(42);
