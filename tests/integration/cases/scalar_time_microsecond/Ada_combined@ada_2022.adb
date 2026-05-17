with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("exact_millisecond", AStr ("09:30:15.123000")),
        AEntry ("sub_millisecond", AStr ("09:30:15.123456"))
    ];
begin
    my_data := AMap'[
        AEntry ("exact_millisecond", AStr ("09:30:15.123000")),
        AEntry ("sub_millisecond", AStr ("09:30:15.123456"))
    ];
end Main;
