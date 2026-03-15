"""
Run every query from household_dashboard in isolation to find the one that fails.
"""
import sys, traceback
sys.path.insert(0, '.')
from datetime import datetime
from app.config.database import get_supabase

db = get_supabase()
u = db.table('users').select('*').eq('phone', '9999900003').execute().data[0]
user_id = u['id']
current_month = datetime.now().strftime('%Y-%m')
print('user_id:', user_id)

# Query 1: workers with join
print('\n--- Query 1: household_workers + users!worker_id join ---')
try:
    r = db.table('household_workers').select('id, worker_id, worker_role, monthly_salary, payment_day, users!worker_id(full_name)').eq('household_id', user_id).eq('is_active', True).execute()
    print('OK:', r.data)
    workers_data = r.data
except Exception as e:
    traceback.print_exc()
    workers_data = []

if workers_data:
    w = workers_data[0]
    worker_id = w['worker_id']

    # Query 2: last payment (no type)
    print('\n--- Query 2: last payment (no payment_type) ---')
    try:
        r = db.table('payments').select('amount_inr, payment_date, payment_month, status').eq('household_id', user_id).eq('worker_id', worker_id).eq('status', 'processed').order('payment_date', desc=True).limit(1).execute()
        print('OK:', r.data)
    except Exception as e:
        traceback.print_exc()

    # Query 3: march_paid with filter
    print('\n--- Query 3: march_paid filter ---')
    try:
        r = db.table('payments').select('id').eq('household_id', user_id).eq('worker_id', worker_id).eq('payment_month', current_month).filter('status', 'in', '("processed","pending")').execute()
        print('OK:', r.data)
    except Exception as e:
        traceback.print_exc()

print('\nALL DONE')
