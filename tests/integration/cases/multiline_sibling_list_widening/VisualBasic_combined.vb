Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Dictionary(Of String, Object) From {
            {"omap_value", New Dictionary(Of String, Object) From {{"first", 1}}},
            {"sibling_lists", New Dictionary(Of String, Object) From {{"numbers", New Object() {1, 2}}, {"strings", New Object() {"x", "y"}}}},
            {"ref_marker_present", New String() {"$keep", "z"}}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Dictionary(Of String, Object) From {
            {"omap_value", New Dictionary(Of String, Object) From {{"first", 1}}},
            {"sibling_lists", New Dictionary(Of String, Object) From {{"numbers", New Object() {1, 2}}, {"strings", New Object() {"x", "y"}}}},
            {"ref_marker_present", New String() {"$keep", "z"}}
        }
    End Sub
End Module
