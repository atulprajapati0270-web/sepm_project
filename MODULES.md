# Module-wise Development Map

Each module has its own Flask blueprint under `app/<module>/routes.py`.

| Module | Blueprint / URL | Main database table |
|---|---|---|
| User Registration & Login | `/auth` | `users` |
| Traffic & Routes | `/traffic` | `routes` |
| Accommodation | `/accommodation` | `accommodations` |
| Food Facilities | `/food` | `food_facilities` |
| Medical Emergency | `/medical` | `medical_facilities` |
| Events & Programmes | `/events` | `events` |
| Shahi Snan | `/shahi-snan` | `shahi_snans` |
| Security & Safety | `/security` | `security_info` |
| Famous/Nearby Temples | `/temples` | `temples` |
| Emergency Helpline | `/emergency` | `emergency_helplines` |
| Complaints | `/complaints` | `complaints` |
| Lost & Found | `/lost-found` | `lost_found` |
| Notifications | `/notifications` | `notifications` |
| Admin Management | `/admin` | all official tables + `admin_logs` |

## What is implemented
- Visitor registration/login/logout
- Password hashing
- Visitor profile update
- Search for information modules
- Complaint submission and status tracking
- Lost & Found submission and status tracking
- Admin authentication and authorization
- Admin CRUD for official information modules
- Admin complaint/Lost & Found status management
- Basic admin counts/reporting
- Administrative action logging
- MySQL-ready database
- GitHub/Render deployment files

## SRS alignment
The module set follows the 14 system features in Section 4 of the supplied SRS. The SRS identifies MySQL as the database option and Flask/Django as suitable backend options. This implementation selects Flask + MySQL.
