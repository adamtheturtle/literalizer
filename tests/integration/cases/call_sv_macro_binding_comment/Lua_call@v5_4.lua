function make_widget(...) end
local my_data = (`__LINE__ > 0) ? make_widget(42) : make_widget(42) // trailing `marker
