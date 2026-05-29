# CLAUDE.md — BalconySlippers (Tapocki)

## Overview
Demo Flask storefront for slippers. Reference template for future clothing/shoe shop projects.
- **Stack:** Flask + in-memory dict DB (no external DB required) + Flask-Login
- **Port:** 5004
- **Venv:** uses `/home/ari-clothes/venv` (shared)

## Commands
```bash
cd /home/tapocki
/home/ari-clothes/venv/bin/python run.py   # dev server port 5004
./start.sh                                  # background launch
```

## Notes
- In-memory DB — all data resets on restart (demo only, not for production)
- No external dependencies (MongoDB removed, replaced with dict-based storage)
- Admin credentials: admin@balconyslippers.com / admin123
