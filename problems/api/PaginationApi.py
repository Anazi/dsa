"""
Design a pagination API:

get_products(page, limit, search=None, sort_by=None, order="asc")

Supports:
- Pagination
- Filtering (by substring)
- Sorting (name, price)
Returns:
{
    "items": [...],
    "total": N,
    "page": page,
    "total_pages": ...,
    "has_next": True/False
}
"""


class ProductAPI:
    def __init__(self, products):
        # products = list of dicts: {"id":1, "name":"A", "price":10}
        self.products = products

    def get_products(self, page, limit, search=None, sort_by=None, order="asc"):
        items = self.products

        # Filtering (search by name)
        if search:
            items = [p for p in items if search.lower() in p["name"].lower()]

        # Sorting
        if sort_by:
            reverse_order = (order == "desc")
            items = sorted(items, key=lambda p: p[sort_by], reverse=reverse_order)

        total = len(items)
        total_pages = (total + limit - 1) // limit  # ceil division

        # Pagination slicing
        start = (page - 1) * limit
        end = start + limit
        paginated_items = items[start:end]

        return {
            "items": paginated_items,
            "total": total,
            "page": page,
            "total_pages": total_pages,
            "has_next": page < total_pages
        }


# ------------------ TEST -------------------

products = [
    {"id": 1, "name": "Apple", "price": 3},
    {"id": 2, "name": "Banana", "price": 1},
    {"id": 3, "name": "Carrot", "price": 2},
    {"id": 4, "name": "Apricot", "price": 5},
    {"id": 5, "name": "Avocado", "price": 4}
]

api = ProductAPI(products)
print(api.get_products(page=1, limit=2, search="a", sort_by="price"))
print(api.get_products(page=2, limit=2, search="a", sort_by="price"))
print(api.get_products(page=3, limit=2, search="a", sort_by="price"))
print(api.get_products(page=4, limit=2, search="a", sort_by="price"))
