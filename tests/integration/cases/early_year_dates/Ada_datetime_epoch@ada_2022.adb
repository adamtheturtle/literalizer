with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("date", AStr ("0099-05-27")),
        AEntry ("naive", AInt (-62135551800)),
        AEntry ("recent", AInt (1716804000))
    ];
begin
    null;
end Main;
