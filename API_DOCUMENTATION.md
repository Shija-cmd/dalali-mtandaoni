\# DALALI MTANDAONI API DOCUMENTATION



\## Version

1.0



\## Base URL



```

http://127.0.0.1:8000/

```



Production URL (Render):



```

https://your-domain.onrender.com/

```



\---



\# Authentication



Protected APIs require an authentication token.



Header:



```

Authorization: Token YOUR\_TOKEN

```



Example:



```

Authorization: Token "..."

```



\---



\# PUBLIC APIs



These APIs do not require login.



\---



\## 1. Home



\*\*GET\*\*



```

/api/home/

```



Returns:



\- Featured Listings

\- Recent Listings

\- Categories



Authentication:



```

No

```



\---



\## 2. Categories



\*\*GET\*\*



```

/api/categories/

```



Returns all categories.



Authentication:



```

No

```



\---



\## 3. Listings



\*\*GET\*\*



```

/api/listings/

```



Supports:



| Parameter | Description |

|------------|-------------|

| q | Search title or description |

| category | Category ID |

| location | Filter by location |

| min\_price | Minimum price |

| max\_price | Maximum price |

| ordering | Sort results |

| page | Pagination |



Example:



```

/api/listings/?category=2\&location=Mbeya

```



Authentication:



```

No

```



\---



\## 4. Listing Details



\*\*GET\*\*



```

/api/listings/<listing\_id>/

```



Returns details for one listing.



Authentication:



```

No

```



\---



\## 5. Featured Listings



\*\*GET\*\*



```

/api/featured-listings/

```



Authentication:



```

No

```



\---



\## 6. Recent Listings



\*\*GET\*\*



```

/api/recent-listings/

```



Authentication:



```

No

```



\---



\## 7. Search Listings



\*\*GET\*\*



```

/api/search/?q=house

```



Authentication:



```

No

```



\---



\# AUTHENTICATION APIs



\---



\## 8. Register



\*\*POST\*\*



```

/api/register/

```



Fields



\- username

\- phone\_number

\- password1

\- password2



Authentication:



```

No

```



\---



\## 9. Login



\*\*POST\*\*



```

/api/login/

```



Fields



\- username

\- password



Returns



```

{

&#x20;   "token": "...",

&#x20;   "username": "...",

&#x20;   "user\_id": 1

}

```



Authentication:



```

No

```



\---



\## 10. Logout



\*\*POST\*\*



```

/api/logout/

```



Authentication:



```

Required

```



\---



\# USER APIs



\---



\## 11. Dashboard



\*\*GET\*\*



```

/api/dashboard/

```



Returns:



\- Total Listings

\- Approved Listings

\- Pending Listings

\- Favorites

\- Verification Status



Authentication:



```

Required

```



\---



\## 12. My Profile



\*\*GET\*\*



```

/api/my-profile/

```



Authentication:



```

Required

```



\---



\## 13. Update Profile



\*\*PUT\*\*



```

/api/my-profile/update/

```



Authentication:



```

Required

```



\---



\## 14. Change Password



\*\*POST\*\*



```

/api/change-password/

```



Fields



\- old\_password

\- new\_password



Authentication:



```

Required

```



\---



\# LISTING APIs



\---



\## 15. Create Listing



\*\*POST\*\*



```

/api/create-listing/

```



Authentication:



```

Required

```



\---



\## 16. Update Listing



\*\*PUT\*\*



```

/api/listings/<listing\_id>/update/

```



Authentication:



```

Required

```



\---



\## 17. Delete Listing



\*\*DELETE\*\*



```

/api/listings/<listing\_id>/delete/

```



Authentication:



```

Required

```



\---



\## 18. Upload Listing Image



\*\*POST\*\*



```

/api/listings/<listing\_id>/upload-image/

```



Authentication:



```

Required

```



\---



\## 19. My Listings



\*\*GET\*\*



```

/api/my-listings/

```



Authentication:



```

Required

```



\---



\## 20. Listing Status



\*\*GET\*\*



```

/api/listing-status/

```



Returns:



\- Listing ID

\- Title

\- Approved Status

\- Active Status



Authentication:



```

Required

```



\---



\# FAVORITES APIs



\---



\## 21. Toggle Favorite



\*\*POST\*\*



```

/api/favorite/<listing\_id>/

```



Authentication:



```

Required

```



\---



\## 22. My Favorites



\*\*GET\*\*



```

/api/my-favorites/

```



Authentication:



```

Required

```



\---



\# VERIFICATION APIs



\---



\## 23. Request Verification



\*\*POST\*\*



```

/api/request-verification/

```



Authentication:



```

Required

```



\---



\## 24. Verification Status



\*\*GET\*\*



```

/api/verification-status/

```



Authentication:



```

Required

```



\---



\## 25. My Verification Requests



\*\*GET\*\*



```

/api/my-verification-requests/

```



Authentication:



```

Required

```



\---



\# OWNER APIs



\---



\## 26. Owner Profile



\*\*GET\*\*



```

/api/owners/<owner\_id>/

```



Returns



\- Owner Information

\- Owner Listings



Authentication:



```

No

```



\---



\# ADMIN APIs



\---



\## 27. Admin Statistics



\*\*GET\*\*



```

/api/admin/statistics/

```



Returns



\- Total Users

\- Verified Users

\- Categories

\- Listings

\- Approved Listings

\- Pending Listings

\- Featured Listings



Authentication:



```

Superuser Only

```



\---



\# Pagination



Listings API supports pagination.



Example



```

/api/listings/?page=2

```



\---



\# HTTP Status Codes



| Code | Meaning |

|------|----------|

|200|Success|

|201|Created|

|400|Bad Request|

|401|Unauthorized|

|403|Forbidden|

|404|Not Found|



\---



\# Technology Stack



\- Django

\- Django REST Framework

\- Token Authentication

\- PostgreSQL

\- Bootstrap 5

\- Pillow

\- Flutter (Mobile Client)



\---



© 2026 DALALI MTANDAONI

