function process {}
$my_var = 42
$my_other = 7
process(@(@{"ref" = "my_var"}; 42; "static"))
process(@(@{"ref" = "my_other"}; 7; "label"))
