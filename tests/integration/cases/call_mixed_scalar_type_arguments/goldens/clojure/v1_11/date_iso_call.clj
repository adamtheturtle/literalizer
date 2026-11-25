(defn capture [& _args] nil)
(capture :nan_value Double/NaN :positive_infinity Double/POSITIVE_INFINITY :negative_infinity Double/NEGATIVE_INFINITY :finite_value 1.25 :date_value "2024-01-15" :datetime_value "2024-01-15T12:34:56" :text_value "[ordinary text]")
