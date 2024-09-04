import ifcopenshell
import openpyxl

ifc_name = "phoenix_statika.ifc"

# Loading IFC
ifc_file = ifcopenshell.open(ifc_name)

# Get all types defined in the schema
schema_types = ifc_file.schema


# Collect types with instances in the file
# ! This is where the types of structures can be seen
types_with_instances = set()

for entity in ifc_file:
    types_with_instances.add(entity.is_a())

# List all types that have instances
for type_name in sorted(types_with_instances):
    print(type_name)

# Separation
print("\n-------------------------------------------\n")

# Filter and list specific types, e.g., only those starting with 'IfcWall'
types_with_instances = set()
for entity in ifc_file:
    if entity.is_a().startswith("IfcWall"):
        types_with_instances.add(entity.is_a())

# Print the filtered types
for type_name in sorted(types_with_instances):
    print(type_name)


# Define the desired types
desired_types = [
    "IfcBeam",
    "IfcColumn",
    "IfcSlab",
    "IfcWall",
]

# Define the desired quantities
desired_quantities = [
    "Length",
    "Bottom Area",
    "Profile Height",
    "Profile Width",
    "Volume",
]

# To store results
results = []


# Function to extract and store the quantities
def extract_quantities(element):
    element_data = {"ID": element.GlobalId, "Type": element.is_a()}

    # Iterate through the defined properties of the element
    for definition in element.IsDefinedBy:
        if hasattr(definition, "RelatingPropertyDefinition"):
            relating_def = definition.RelatingPropertyDefinition
            if relating_def.is_a("IfcElementQuantity"):
                quantities = relating_def.HasQuantities
                for quantity in quantities:
                    quantity_name = quantity.Name
                    if quantity_name in desired_quantities:
                        element_data[quantity_name] = quantity.NominalValue

    results.append(element_data)


# Iterate through the IFC file elements and filter by the desired types
for ifc_type in desired_types:
    elements = ifc_file.by_type(ifc_type)
    for element in elements:
        extract_quantities(element)

# Print out the results
for result in results:
    print(f"Element ID: {result['ID']}, Type: {result['Type']}")
    for quantity in desired_quantities:
        if quantity in result:
            print(f"  {quantity}: {result[quantity]}")
    print()  # Add a blank line for better readability


# Create an Excel workbook and add a worksheet
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "IFC Quantities"

# Write headers to the Excel file
headers = ["Element ID", "Type"] + desired_quantities
ws.append(headers)

# Write data rows to the Excel file
for result in results:
    row = [result.get("ID"), result.get("Type")]
    for quantity in desired_quantities:
        row.append(result.get(quantity))
    ws.append(row)

# Save the Excel file
output_file = "ifc_quantities.xlsx"
wb.save(output_file)
print(f"Data successfully written to {output_file}")
