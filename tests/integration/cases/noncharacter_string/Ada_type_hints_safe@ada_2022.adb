with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("fffe", AStr ("￾")),
        AEntry ("ffff", AStr ("￿"))
    ];
begin
    null;
end Main;
