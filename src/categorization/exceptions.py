class ParentCategoryMissingError(Exception):
    """
    Exception for attempts to add sub-categories when no parent exists
    """
    pass

class SubCategorySameAsParentError(Exception):
    """
    Exception for sub categories being the same as a parent category.
    """
    pass