(defn process [& _args] nil)
(process :value 1 :extra "hello")
(process :value "two" :extra false)
(process :value 3.5 :extra nil)
