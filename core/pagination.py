from rest_framework.pagination import CursorPagination


class ProductCursorPagination(CursorPagination):
    """
    Cursor-based pagination is used to efficiently paginate through large, changing datasets.
    Instead of using page numbers (which can be slow and skip items if new records are added),
    it remembers the "cursor" position of the last seen item.
    """
    
    # Specifies the default number of items to return per page
    page_size = 12

    # Tells the paginator to order the results by the 'created_at' field in descending order
    # so the newest items are shown first.
    ordering = "-created_at"