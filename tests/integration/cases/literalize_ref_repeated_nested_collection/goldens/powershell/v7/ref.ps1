$Shared = @(
    ,@(1; 2);
    @{"value" = 1}
)
$my_data = @(
    $Shared;
    $Shared
)
