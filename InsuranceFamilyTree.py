class FamilyTreeNode:
    def __init__(self, patient=None):
        self.patient = patient  # Initialize the patient data for this node
        self.children = []  # Initialize a list to store child nodes


class InsuranceFamilyTree:
    def __init__(self):
        self.root = FamilyTreeNode()  # Initialize the root node of the family tree

    def add_family(self, primary_patient, insurance_info=None):
        # Add a new family to the family tree with a primary patient and optional insurance information
        new_family_node = FamilyTreeNode(primary_patient)
        primary_patient.insurance_info = insurance_info  # Assign insurance information to the primary patient
        self.root.children.append(new_family_node)  # Add the new family as a child of the root node
        return new_family_node  # Return the new family node

    def add_family_member(self, family_node, new_member):
        # Add a new family member to an existing family node
        new_member_node = FamilyTreeNode(new_member)
        new_member.primary_member = family_node.patient  # Set the primary member of the new member

        # Copy insurance information from the primary member to the new member if it exists
        if family_node.patient.insurance_info:
            new_member.insurance_info = family_node.patient.insurance_info

        family_node.children.append(new_member_node)  # Add the new member node to the family node

    def find_member(self, first_name, last_name):
        # Find and return a family member node by their first name and last name
        for family in self.root.children:
            if family.patient.first_name == first_name and family.patient.last_name == last_name:
                return family
            for member in family.children:
                if member.patient.first_name == first_name and member.patient.last_name == last_name:
                    return member
        return None  # Return None if the member is not found

    def print_family_tree(self):
        # Print the entire family tree starting from the root node
        for family in self.root.children:
            self.print_node(family, 0)

    def print_node(self, node, level):
        # Print a node and its children with proper indentation
        indent = '   ' * level
        print(f"{indent}{node.patient.first_name} {node.patient.last_name}")
        for child in node.children:
            self.print_node(child, level + 1)
