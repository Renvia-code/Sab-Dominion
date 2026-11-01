// Query LoadGrowth (Import)
let
    Source = Excel.Workbook(File.Contents(DataFolder & "Dominion_Reliability_PowerBI_Data.xlsx"), null, true),
    LoadGrowth_Sheet = Source{[Item="LoadGrowth",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(LoadGrowth_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"year", Int64.Type}, {"commercial_twh", type number}, {"residential_twh", type number}, {"commercial_customers", Int64.Type}, {"residential_customers", Int64.Type}, {"commercial_sales_index", type number}, {"commercial_customers_index", type number}, {"residential_sales_index", type number}, {"Column9", type any}, {"Source", type text}})
in
    #"Changed Type"
