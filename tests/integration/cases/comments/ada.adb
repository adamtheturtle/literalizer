procedure Check is
   X : Integer := AMap'(
       -- Server configuration
       AEntry ("host", AStr ("localhost")),  -- default host
       AEntry ("port", AInt (8080)),
       -- Enable debug mode
       AEntry ("debug", ABool (True))
   );
begin
   null;
end Check;
