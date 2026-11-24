(create-ns 'throttler)
(intern 'throttler 'check (fn [& _args] nil))
(throttler/check)
(throttler/check)
