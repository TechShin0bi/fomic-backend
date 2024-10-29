from plan.models import Plan

plans_part1 = [
    {"name": "VIP 1", "price": 5000, "daily_revenue": 355, "duration": 90, "category": "1"},
    {"name": "VIP 2", "price": 10000, "daily_revenue": 710, "duration": 90, "category": "1"},
    {"name": "VIP 3", "price": 12000, "daily_revenue": 852, "duration": 90, "category": "1"},
    {"name": "VIP 4", "price": 20000, "daily_revenue": 1420, "duration": 90, "category": "1"},
    {"name": "VIP 5", "price": 40000, "daily_revenue": 2840, "duration": 90, "category": "1"},
    {"name": "VIP 6", "price": 50000, "daily_revenue": 3550, "duration": 90, "category": "1"},
    {"name": "VIP 7", "price": 100000, "daily_revenue": 7100, "duration": 90, "category": "1"},
]

plans_part2 = [
    {"name": "VIP 8", "price": 200000, "daily_revenue": 14200, "duration": 90, "category": "2"},
    {"name": "VIP 9", "price": 300000, "daily_revenue": 21300, "duration": 90, "category": "2"},
    {"name": "VIP 10", "price": 400000, "daily_revenue": 28400, "duration": 90, "category": "2"},
    {"name": "VIP 11", "price": 500000, "daily_revenue": 35500, "duration": 90, "category": "2"},
    {"name": "VIP 12", "price": 1000000, "daily_revenue": 71000, "duration": 90, "category": "2"},
    {"name": "VIP 13", "price": 2000000, "daily_revenue": 142000, "duration": 90, "category": "2"},
]

for plan in plans_part1 + plans_part2:
    Plan.objects.create(**plan)
