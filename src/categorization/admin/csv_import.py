from django.core.exceptions import ObjectDoesNotExist
import csv
import os
from src.categorization.models import Category

BASE_DIR = os.path.dirname(__file__)

class CSVCategory:
    def __init__(self, row_data):
        self.name = row_data[0]
        self.parent_category_name = row_data[1]
        self.hashtag = row_data[2]
        self.banner_url = row_data[3]
        self.is_primary_category = len(self.parent_category_name) < 1

        if self.is_primary_category:
            self.children = []

    def add_child(self, category):
        self.children.append(category)


def get_categories_from_csv():
    dict_to_return = {}

    with open(os.path.join(os.path.dirname(__file__), "Pre-Defined Categories - Import.csv"), 'r') as file:

        reader = csv.reader(file)
        for row_num, row in enumerate(reader):
            # Skip the first row, Header Row
            if row_num == 0:
                continue

            category = CSVCategory(row)
            if category.is_primary_category:
                dict_to_return[category.name] = category
            else:
                dict_to_return[category.parent_category_name].add_child(category)

    return dict_to_return


def __update_or_add_child_category(parent_category, child_category):
    try:
        child = Category.objects.get(name=child_category.name)
        child.thumbnail_large = child_category.banner_url
        child.hashtag = child_category.hashtag
        child.parent_category = parent_category
        child.save()
    except ObjectDoesNotExist:
        child = Category.objects.create(name=child_category.name,
                                        hashtag=child_category.hashtag,
                                        thumbnail_large=child_category.banner_url,
                                        is_active=True, parent_category=parent_category)
        child.save()




def import_categories(should_overwrite=False):
    categories = get_categories_from_csv()
    for key, parent_category in categories.items():
        try:
            parent = Category.objects.get(name=key)
            parent.thumbnail_large = parent_category.banner_url
            parent.hashtag = parent_category.hashtag
            parent.save()
        except ObjectDoesNotExist:
            parent = Category.objects.create(name=parent_category.name,
                                                 thumbnail_large=parent_category.banner_url,
                                                 is_active=True)
            parent.save()
        finally:
            for child in parent_category.children:
                __update_or_add_child_category(parent, child)





if __name__ == "__main__":
    import_categories()