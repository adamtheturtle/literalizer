with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("morning", AStr ("09:30:00")),
        AEntry ("afternoon", AStr ("14:15:00")),
        AEntry ("evening", AStr ("23:59:59"))
    ];
begin
    null;
end Main;
