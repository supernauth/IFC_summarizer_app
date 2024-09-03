"""
Extracting information about material layers and thickness from IFC file using python
https://medium.com/@talha.siddiqui767/extracting-information-about-material-layers-and-thickness-from-ifc-file-using-python-e86ee001dfde
"""

"""
Information related to material layers and thickness pertaining to a wall or a
floor can be useful for a number of reasons.
It can give you a very good idea about thermal resistance of a wall or it can
use in the calculation of thermal transmittance values.
In my case, I wanted to use these values for developing a recommender system
for buildings.
Anyways, in this post i want to provide a code I used to successfully extract
the material layers and thickness information.
"""

# Step 1: Import the “ifcopenshell” module
import ifcopenshell

"""
This module is needed to work with IFC (Industry Foundation Classes) files,
which are used in the construction industry
to store information about building components.
"""

# Step 2: Open the IFC file
ifc_file = ifcopenshell.open("D:/my_file.ifc")

"""
This step opens the IFC file located at the specified file path.
"""

# Step 3: Get all IFCWALL elements in the file
ifc_walls = ifc_file.by_type("IFCWALL")

"""
This step retrieves all the IFCWALL elements in the IFC file. “by_type”
is a method of the “ifc_file” object,
which returns a generator object containing all the elements of the
specified type.
"""


# Step 4: Define a function to get the materials and thickness of an element
def get_ifc_materials_and_thickness(ifc_element):
    material_thickness_list = []

"""
This step defines a function named “get_ifc_materials_and_thickness”
that takes an IFC element as input and returns
a list of tuples containing the names and thicknesses of the
materials used in the element.
"""

# Step 5: Check if the element has a material
ifc_material = ifcopenshell.util.element.get_material(ifc_element)

"""
This step checks if the IFC element has a material defined. The
“get_material” function is a utility 
unction provided by the “ifcopenshell” module that returns the
material associated with the given element, if any.
"""

# Step 6: Append material names and thicknesses to the list

if ifc_material:
    if ifc_material.is_a('IfcMaterial'):
        # If the material is an IfcMaterial entity, append its name and thickness (if available)
        material_thickness_list.append((ifc_material.Name, ifc_material.Thickness))
    elif ifc_material.is_a('IfcMaterialLayerSetUsage'):
        # If the material is a layer set usage, loop over the layers and append their names and thicknesses
        for layer in ifc_material.ForLayerSet.MaterialLayers:
            material_thickness_list.append((layer.Material.Name, layer.LayerThickness))
            
"""
This step checks the type of material associated with the element, and appends
the material name and thickness to the “material_thickness_list” if it is an
“IfcMaterial” entity. If the material is a “IfcMaterialLayerSetUsage”, it loops
over the layers and appends their names and thicknesses to the list. If the
material is not an “IfcMaterial” or “IfcMaterialLayerSetUsage”, only the
material type is appended to the list.
"""

# Step 7: Append None values if no material is found

else:
    # If the material is not an IfcMaterial or a layer set usage, just append its type and None for thickness
    material_thickness_list.append((type(ifc_material).__name__, None))
    else:
        # If no material is found, append None for both material and thickness
        material_thickness_list.append((None, None))
        
"""
If no material is found for the element, the function appends None values for
both material name and thickness to the list.
"""

# Step 8: Iterate over all IFCWALL elements and store their materials and thickness in a list of dictionaries

walls_data = []
for wall in ifc_walls:
    materials_and_thickness = get_ifc_materials_and_thickness(wall)
    wall_tag = wall.get_info()['Name']
    wall_data = {wall_tag: materials_and_thickness}
    walls_data.append(wall_data)
    
"""
This step iterates over all the IFCWALL elements and calls the 
"get_ifc_materials_and_thickness” function to retrieve the material
names and thicknesses associated with each wall. The material names
and thicknesses are stored in a dictionary object, where the key is
the name of the wall (retrieved using the “get_info” function), and
the value is the list of materials and thicknesses. The dictionary
is then appended to the “walls_data” list.

The above steps will give you a list containing the layers contained
in a wall and its corresponding materials and also the thicknesses
of each of these materials. I hope this may help someone who is
working on something and needs to use information related to wall
materials and thickness
"""