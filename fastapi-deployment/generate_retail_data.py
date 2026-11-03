#!/usr/bin/env python3
"""Generate retail order NDJSON files matching retail_orders_sample.json.
Install: python -m pip install Faker
Run:    python generate_retail_data.py
"""
import argparse
import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path
from faker import Faker

fake = Faker("en_IN")

STORES = [
    ("ST-001", "Hyderabad Central", "Hyderabad", "Telangana", "SOUTH", "500081"),
    ("ST-002", "Bengaluru South", "Bengaluru", "Karnataka", "SOUTH", "560001"),
    ("ST-003", "Chennai Marina", "Chennai", "Tamil Nadu", "SOUTH", "600001"),
    ("ST-004", "Pune West", "Pune", "Maharashtra", "WEST", "411004"),
    ("ST-005", "Delhi North", "Delhi", "Delhi", "NORTH", "110009"),
    ("ST-006", "Kochi Marine Drive", "Kochi", "Kerala", "SOUTH", "682011"),
    ("ST-007", "Jaipur City", "Jaipur", "Rajasthan", "NORTH", "302001"),
    ("ST-008", "Mumbai Central", "Mumbai", "Maharashtra", "WEST", "400001"),
]
PRODUCTS = [
    ("Wireless Mouse", "Electronics", "Accessories", "LogiTech", 799, {"color": ["Black", "White", "Blue"], "connectivity": ["Bluetooth", "USB"]}),
    ("USB-C Cable", "Electronics", "Cables", "CablePro", 399, {"color": ["White", "Black"], "length": ["1m", "2m"]}),
    ("Running Shoes", "Fashion", "Footwear", "Stride", 3499, {"color": ["Blue", "Black"], "size": ["7", "8", "9", "10"]}),
    ("Coffee Maker", "Home", "Appliances", "BrewWell", 2499, {"color": ["Silver", "Black"], "capacity": ["1L", "1.2L"]}),
    ("Bluetooth Speaker", "Electronics", "Audio", "SoundPeak", 1999, {"color": ["Red", "Black"], "waterproof": [True, False]}),
    ("Notebook Set", "Stationery", "Paper", "WriteRight", 120, {"pages": [100, 200, 300], "paper_type": ["Ruled", "Plain"]}),
    ("Yoga Mat", "Sports", "Fitness", "FlexFit", 899, {"color": ["Purple", "Green"], "thickness_mm": [4, 6, 8]}),
    ("Air Purifier", "Home", "Appliances", "PureAir", 8999, {"filter_type": ["HEPA", "Carbon"], "room_size_sqft": [250, 450, 600]}),
    ("Replacement Filter", "Home", "Accessories", "PureAir", 1299, {"filter_type": ["HEPA", "Carbon"], "compatible_model": ["PA-250", "PA-450"]}),
    ("Travel Backpack", "Fashion", "Bags", "TrailWay", 1599, {"color": ["Olive", "Black"], "capacity_liters": [20, 32, 40]}),
    ("Smart Watch", "Electronics", "Wearables", "TimeTech", 4999, {"color": ["Black", "Silver"], "water_resistant": [True, False]}),
    ("Water Bottle", "Home", "Kitchen", "HydroPlus", 499, {"color": ["Blue", "Pink"], "capacity_ml": [500, 750, 1000]}),
]
TIERS = ["NEW", "BRONZE", "SILVER", "GOLD", "PLATINUM"]
CHANNELS = ["WEB", "MOBILE_APP", "STORE"]
STATUSES = ["DELIVERED", "DELIVERED", "DELIVERED", "PROCESSING", "PENDING_PAYMENT", "CANCELLED", "RETURNED"]
METHODS = ["UPI", "CARD", "COD", "NET_BANKING", "WALLET"]
CARRIERS = ["BlueDart", "Delhivery", "Ecom Express", "DTDC"]
SOURCES = ["commerce-api", "mobile-commerce", "pos-system"]
PROMOS = ["FESTIVE10", "WELCOME5", "PLAT20", "SAVE15"]

def money(x):
    return round(x + 1e-9, 2)

def stamp(dt):
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def make_customer(customer_id, store):
    gender = random.choice(["F", "M", "OTHER"])
    first = fake.first_name_female() if gender == "F" else fake.first_name_male()
    return {
        "customer_id": customer_id,
        "full_name": f"{first} {fake.last_name()}",
        "email": fake.email(),
        "phone": fake.numerify("+919#########") if random.random() > 0.08 else None,
        "gender": gender,
        "age": random.randint(18, 75),
        "loyalty_tier": random.choice(TIERS),
        "registered_date": fake.date_between("-6y", "today").isoformat(),
        "address": {"line1": fake.street_address(), "city": store[2], "state": store[3],
                    "postal_code": store[5], "country": "India"},
    }

def make_item(line_id):
    p = random.randrange(len(PRODUCTS))
    name, category, subcategory, brand, base, attr_options = PRODUCTS[p]
    qty = random.randint(1, 5)
    price = money(base * random.uniform(0.85, 1.15))
    discount = random.choice([0.0, 0.0, 5.0, 10.0, 15.0, 20.0])
    tax = random.choice([5.0, 12.0, 18.0])
    total = money(price * qty * (1 - discount / 100) * (1 + tax / 100))
    attrs = {k: random.choice(v) for k, v in attr_options.items()}
    return {"line_id": line_id, "product_id": f"PRD-{p+1:03d}", "product_name": name,
            "category": category, "subcategory": subcategory, "brand": brand,
            "quantity": qty, "unit_price": price, "discount_pct": discount,
            "tax_pct": tax, "line_total": total, "attributes": attrs}

def make_order(n, customer_pool, start, end):
    s = random.choice(STORES)
    order_dt = fake.date_time_between(start_date=start, end_date=end, tzinfo=timezone.utc)
    status = random.choice(STATUSES)
    items = [] if random.random() < 0.015 else [make_item(i + 1) for i in range(random.randint(1, 5))]
    subtotal = money(sum(x["unit_price"] * x["quantity"] for x in items))
    discount = money(sum(x["unit_price"] * x["quantity"] * x["discount_pct"] / 100 for x in items))
    tax = money(sum(x["unit_price"] * x["quantity"] * (1-x["discount_pct"]/100) * x["tax_pct"]/100 for x in items))
    shipping_fee = 0.0 if subtotal >= 3000 or not items else float(random.choice([30, 40, 50, 60, 80]))
    total = money(subtotal - discount + tax + shipping_fee)

    if status == "CANCELLED":
        pay_status, ship_status = "VOIDED", "NOT_SHIPPED"
    elif status == "PENDING_PAYMENT":
        pay_status, ship_status = "PENDING", "NOT_SHIPPED"
    elif status == "PROCESSING":
        pay_status, ship_status = random.choice(["AUTHORIZED", "CAPTURED"]), "NOT_SHIPPED"
    elif status == "RETURNED":
        pay_status, ship_status = "REFUNDED", "RETURNED"
    else:
        pay_status, ship_status = "CAPTURED", "DELIVERED" if items else "NOT_REQUIRED"

    carrier = random.choice(CARRIERS) if ship_status in ("DELIVERED", "RETURNED") else None
    tracking = f"TR{fake.random_number(digits=10, fix_len=True)}" if carrier else None
    shipped = order_dt + timedelta(hours=random.randint(2, 36)) if carrier else None
    delivered = shipped + timedelta(hours=random.randint(8, 72)) if shipped else None

    events = [{"event_type": "PLACED", "event_ts": stamp(order_dt)}]
    if pay_status in ("AUTHORIZED", "CAPTURED", "REFUNDED"):
        events.append({"event_type": "PAYMENT_" + pay_status, "event_ts": stamp(order_dt + timedelta(minutes=3))})
    if shipped:
        events.append({"event_type": "SHIPPED", "event_ts": stamp(shipped)})
    if delivered:
        events.append({"event_type": "DELIVERED", "event_ts": stamp(delivered)})
    if status in ("CANCELLED", "RETURNED"):
        event_dt = (delivered or order_dt) + timedelta(days=2) if status == "RETURNED" else order_dt + timedelta(minutes=30)
        events.append({"event_type": status, "event_ts": stamp(event_dt)})
    events.sort(key=lambda x: x["event_ts"])

    promotions = []
    if discount > 0 and random.random() < 0.65:
        promotions.append({"promo_code": random.choice(PROMOS), "promo_type": "PERCENT", "discount_amount": discount})
    if shipping_fee > 0 and random.random() < 0.12:
        promotions.append({"promo_code": "FREESHIP", "promo_type": "SHIPPING", "discount_amount": shipping_fee})

    return {
        "order_id": f"ORD-{order_dt.year}-{n:08d}",
        "order_ts": stamp(order_dt),
        "order_date": order_dt.date().isoformat(),
        "order_status": status,
        "sales_channel": random.choice(CHANNELS),
        "store": {"store_id": s[0], "store_name": s[1], "city": s[2], "state": s[3], "country": "India", "region": s[4]},
        "customer": make_customer(f"CUST-{random.randint(1, customer_pool):05d}", s),
        "items": items,
        "payment": {"payment_id": f"PAY-{900000+n:09d}", "method": random.choice(METHODS),
                    "status": pay_status, "currency": "INR", "subtotal": subtotal,
                    "discount_amount": discount, "tax_amount": tax, "shipping_fee": shipping_fee,
                    "total_amount": total},
        "shipping": {"carrier": carrier, "tracking_id": tracking, "shipping_status": ship_status,
                     "shipped_ts": stamp(shipped) if shipped else None,
                     "delivered_ts": stamp(delivered) if delivered else None,
                     "shipping_address": {"city": s[2], "state": s[3], "postal_code": s[5], "country": "India"}},
        "promotions": promotions,
        "order_events": events,
        "is_gift": random.random() < 0.12,
        "source_system": random.choice(SOURCES),
        "ingest_ts": stamp(order_dt + timedelta(seconds=random.randint(1, 120))),
    }

def main():
    parser = argparse.ArgumentParser(description="Generate retail sales JSON Lines files.")
    parser.add_argument("--files", type=int, default=10)
    parser.add_argument("--records-per-file", type=int, default=50000)
    parser.add_argument("--output-dir", default="retail-data")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--customers", type=int, default=20000, help="Size of reusable customer ID pool")
    parser.add_argument("--start-date", default="2025-01-01")
    parser.add_argument("--end-date", default="2026-11-08")
    args = parser.parse_args()
    if min(args.files, args.records_per_file, args.customers) < 1:
        parser.error("files, records-per-file and customers must be positive integers")

    random.seed(args.seed)
    Faker.seed(args.seed)
    fake.seed_instance(args.seed)
    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    start = datetime.strptime(args.start_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    end = datetime.strptime(args.end_date, "%Y-%m-%d").replace(hour=23, minute=59, second=59, tzinfo=timezone.utc)
    if end < start:
        parser.error("end-date must be on or after start-date")

    order_num = 1
    total = args.files * args.records_per_file
    print(f"Generating {total:,} records...")
    for file_num in range(1, args.files + 1):
        path = outdir / f"orders_{file_num:03d}.json"
        with path.open("w", encoding="utf-8") as f:
            for _ in range(args.records_per_file):
                row = make_order(order_num, args.customers, start, end)
                f.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")
                order_num += 1
        print(f"Created {path} ({args.records_per_file:,} records)")
    print(f"Done: {args.files} files, {total:,} total records in {outdir.resolve()}")

if __name__ == "__main__":
    main()
