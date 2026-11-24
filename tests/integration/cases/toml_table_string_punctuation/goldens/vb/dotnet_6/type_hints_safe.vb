Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"comma_hash", "a,#b"},
        {"comma_space_hash", "trail, # comment"},
        {"escaped_quote", "quote "" and , #"},
        {"next_line", "x    y"},
        {"line_separator", "x     y"},
        {"paragraph_separator", "x     y"}
    }
End Module
