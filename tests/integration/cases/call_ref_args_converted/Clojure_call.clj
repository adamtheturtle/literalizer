(defn process [& _args] nil)
(def my-var [
    1
    2
    3
])
(def my-other [
    4
    5
    6
])
(process :data my-var :count 42)
(process :data my-other :count 7)
