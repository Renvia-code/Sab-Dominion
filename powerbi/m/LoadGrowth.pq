// Query LoadGrowth (Import)
let
    Source = Csv.Document(File.Contents(DataFolder & "load_growth.csv"), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Selected = Table.SelectColumns(Promoted, {"year", "commercial_twh", "residential_twh", "commercial_customers", "residential_customers", "commercial_sales_index", "commercial_customers_index", "residential_sales_index"}),
    Blanks = Table.ReplaceValue(Selected, "", null, Replacer.ReplaceValue, Table.ColumnNames(Selected)),
    Typed = Table.TransformColumnTypes(Blanks, {{"year", Int64.Type}, {"commercial_twh", type number}, {"residential_twh", type number}, {"commercial_customers", Int64.Type}, {"residential_customers", Int64.Type}, {"commercial_sales_index", type number}, {"commercial_customers_index", type number}, {"residential_sales_index", type number}}, "en-US")
in
    Typed
