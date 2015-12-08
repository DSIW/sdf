def unpublish_book(book):
    offer = book.offer()
    if offer is not None:
        offer.active = False
        offer.save()
