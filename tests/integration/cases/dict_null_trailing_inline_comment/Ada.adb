procedure Check is
    my_data : A_Val := AMap'(
        AEntry ("host", AStr ("localhost")),
        AEntry ("port", ANull)  -- not configured yet
    );
begin
    null;
end Check;
