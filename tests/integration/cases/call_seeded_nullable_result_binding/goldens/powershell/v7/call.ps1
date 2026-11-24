function make_widget {}
function consume {}
$my_data = make_widget $null
consume $my_data
$my_data = make_widget 42
consume $my_data
