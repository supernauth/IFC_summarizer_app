import ifcopenshell

# Load the IFC file
ifc_file = ifcopenshell.open("phoenix_statika.ifc")

# Define the desired types (you can test with one type first, like IfcWall)
sample_type = "IfcColumn"

# Get a sample element of the type
elements = ifc_file.by_type(sample_type)


# Function to print all quantities of a sample element
def print_all_quantities(element):
    print(f"Element ID: {element.GlobalId}, Type: {element.is_a()}")
    for definition in element.IsDefinedBy:
        if hasattr(definition, "RelatingPropertyDefinition"):
            relating_def = definition.RelatingPropertyDefinition
            if relating_def.is_a("IfcElementQuantity"):
                quantities = relating_def.HasQuantities
                for quantity in quantities:
                    print(
                        f"  Quantity Name: {quantity.Name}, Value: {quantity.NominalValue}"
                    )
    print()


# Print quantities for the first element of the sample type
if elements:
    print_all_quantities(elements)
else:
    print("No elements of type", sample_type)
