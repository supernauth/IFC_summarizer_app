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
