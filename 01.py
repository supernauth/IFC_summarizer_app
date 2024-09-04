import ifcopenshell

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


# Function to extract and print the quantities
def extract_quantities(element):
    # Iterate through the defined properties of the element
    for definition in element.IsDefinedBy:
        if hasattr(definition, "RelatingPropertyDefinition"):
            quantities = definition.RelatingPropertyDefinition.HasQuantities
            # Check each quantity
            for quantity in quantities:
                quantity_name = quantity.Name
                if quantity_name in desired_quantities:
                    # Print or store the desired quantities
                    print(
                        f"Element ID: {element.GlobalId}, Type: {element.is_a()}, {quantity_name}: {quantity.NominalValue}"
                    )


# Iterate through the IFC file elements and filter by the desired types
for ifc_type in desired_types:
    elements = ifc_file.by_type(ifc_type)
    for element in elements:
        extract_quantities(element)
