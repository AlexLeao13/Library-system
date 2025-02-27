import openpyxl
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.chart.label import DataLabelList

# Create an Excel workbook and sheet
wb = Workbook()
ws = wb.active
ws.title = "Test Graphique"

# Add test data sorted from highest to lowest
data = [
    ["Subject Area", "Scholarly Output", "Percentage (%)"],
    ["Engineering", 10, 66.7],
    ["Business", 6, 40.0],
    ["Social Sciences", 3, 20.0],
    ["Economics", 2, 13.3],
    ["Arts & Humanities", 1, 6.7]
]

# Sort the data from highest to lowest
sorted_data = [data[0]] + sorted(data[1:], key=lambda x: x[1], reverse=True)

# Reverse the order so that the largest values appear at the top
sorted_data = [sorted_data[0]] + list(reversed(sorted_data[1:]))

# Insert the sorted data into the Excel sheet
for row in sorted_data:
    ws.append(row)

# Define data ranges for the chart
start_row = 2  # Data starts at row 2 (after the header)
end_row = start_row + len(sorted_data) - 2  # Data ends at start_row + number of rows - 1

# Define the data range for the chart (Percentage column)
data_range = Reference(ws, min_col=3, min_row=start_row, max_row=end_row)

# Define the categories range for the chart (Subject Area names)
categories_range = Reference(ws, min_col=1, min_row=start_row, max_row=end_row)

# Create a horizontal bar chart
chart = BarChart()
chart.type = "bar"  # Horizontal bar chart
chart.title = None
chart.y_axis.title = None
chart.x_axis.title = None

# Add data and categories to the chart
chart.add_data(data_range, titles_from_data=False)  # Ensure we don't take the column title
chart.set_categories(categories_range)

# ✅ Ensure percentages appear at the end of each bar with the "%" symbol
if chart.series:
    for series in chart.series:
        series.dLbls = DataLabelList()
        series.dLbls.showVal = True  # Afficher uniquement les valeurs
        series.dLbls.showCatName = True  # Désactiver les noms des catégories
        series.dLbls.showSerName = False  # Désactiver "Series1"
        series.dLbls.position = "outEnd"  # Position labels at the end of bars
        series.dLbls.number_format = "0.0%"


# ✅ Remove the "Series1" legend
chart.legend = None  # Completely remove the legend

# ✅ Restore bar colors
for series in chart.series:
    series.graphicalProperties.solidFill = "4472C4"  # Restore blue color

# ✅ Reverse the Y-axis order to invert labels
chart.y_axis.reverseOrder = True  # Invert label order on the graph
chart.y_axis.tickLblPos = "low"  # Align labels properly

# Style the chart
chart.style = 10  # Apply a predefined style
chart.y_axis.majorGridlines = None  # Remove gridlines
chart.x_axis.majorGridlines = None  # Remove gridlines

# Add the chart to the worksheet
ws.add_chart(chart, "E2")  # Insert the chart starting at cell E2

# Save the Excel file
excel_file_path = "graphique_with_chart.xlsx"
wb.save(excel_file_path)

print(f"The file '{excel_file_path}' has been generated successfully. Open it and check the chart.")
