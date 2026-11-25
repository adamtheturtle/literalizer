with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("date", AStr ("0099-05-27")),
        AEntry ("naive", AStr ("0001-01-01T12:30:00")),
        AEntry ("recent", AStr ("2024-05-27T10:00:00"))
    ];
begin
    null;
end Main;
