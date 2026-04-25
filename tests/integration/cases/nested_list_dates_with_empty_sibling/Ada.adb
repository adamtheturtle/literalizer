procedure Check is
   my_data : A_Val := AList'(
       AList'(AStr ("2026-01-01"), AStr ("2026-01-02")),
       AList'(1 .. 0 => ANull),
       AList'(AStr ("2026-02-03"), AStr ("2026-02-04"))
   );
begin
   null;
end Check;
