Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"sibling_lists", New Dictionary(Of String, Object) From {
            {"numbers", New Object() {
                1,
                2
            }},
            {"strings", New Object() {
                "x",
                "y"
            }}
        }},
        {"ref_marker_present", New String() {
            "$keep",
            "z"
        }}
    }
End Module
