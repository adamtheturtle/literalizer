with A_Stub; use A_Stub;
procedure Main is
    my_time : A_Val := AStr ("01:02:03");
    my_data : A_Val := AMap'[
        AEntry ("x", my_time)
    ];
begin
    null;
end Main;
