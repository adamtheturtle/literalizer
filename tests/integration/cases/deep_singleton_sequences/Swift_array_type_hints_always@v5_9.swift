import Foundation

struct Array {}
let my_data: [String: Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Int>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>] = [
    "deep": [[[[[[({ return [[[[[[[[({ return [[[[[[[[({ return [[[[[[[[1]]]]]]]] })()]]]]]]]] })()]]]]]]]] })()]]]]]],
]
typealias ExpectedLeaf = Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Swift.Array<Int>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
precondition(type(of: my_data) == [String: ExpectedLeaf].self)
let encoded = try JSONSerialization.data(withJSONObject: my_data, options: [.sortedKeys])
let expected = "{\"deep\":[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[1]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]}"
precondition(String(data: encoded, encoding: .utf8) == expected)
