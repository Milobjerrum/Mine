from django.shortcuts import get_object_or_404
from .models import Listing


# def add_remove_watching(user_id)
# def watch_watching(user_id, listing_id):
#     """ Tracking if a user is watching a item"""
#     item = get_object_or_404(Listing, id=listing_id)

#     is_watching = False

#     if item.watch.filter(id=user_id).exists():
#         item.watch.remove(user_id)
#         is_watching = False

#     else:
#         item.watch.add(user_id)
#         is_watching = True
    
#     return is_watching
