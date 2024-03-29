from django.core.paginator import Paginator


def pagination(query, page):  
    paginator = Paginator(query, 6)
    page = int(page or 1)
    query = paginator.page(page)

    # display 3 buttons for pagination
    if page == 1:
        pages = [page, page + 1, page + 2] if int(paginator.num_pages) > 2 else [page, page + 1] 
    elif page == paginator.num_pages:
        pages = [page - 2, page - 1, page] if int(paginator.num_pages) > 2 else [page - 1, page]
    else:
        pages = [page - 1, page, page + 1]

    return paginator.num_pages, pages, query