procedure Check is
    my_data : A_Val := AList'(
        AFloat (1.0 / 0.0),
        AFloat (-1.0 / 0.0),
        AFloat (0.0 / 0.0)
    );
begin
    null;
end Check;
