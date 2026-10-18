with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("half", AStr ("1979-05-27T07:32:00.500000")),
        AEntry ("milli", AStr ("1979-05-27T07:32:00.100000")),
        AEntry ("max_milli", AStr ("1979-05-27T07:32:00.999000")),
        AEntry ("whole", AStr ("1979-05-27T07:32:00"))
    ];
begin
    null;
end Main;
