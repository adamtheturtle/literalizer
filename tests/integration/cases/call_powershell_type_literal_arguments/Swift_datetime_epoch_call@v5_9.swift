import Foundation
@discardableResult func capture(nan_value: Any = 0, positive_infinity: Any = 0, negative_infinity: Any = 0, finite_value: Any = 0, date_value: Any = 0, datetime_value: Any = 0, text_value: Any = 0) -> Any { 0 }
capture(nan_value: Double.nan, positive_infinity: Double.infinity, negative_infinity: -Double.infinity, finite_value: 1.25, date_value: DateComponents(calendar: Calendar(identifier: .gregorian), timeZone: TimeZone(secondsFromGMT: 0)!, year: 2024, month: 1, day: 15).date!, datetime_value: 1705322096, text_value: "[ordinary text]");
