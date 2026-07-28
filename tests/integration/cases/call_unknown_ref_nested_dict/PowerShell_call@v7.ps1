function process {}
$my_list = @()
process(@(,@(@{"inner" = $my_list})))
