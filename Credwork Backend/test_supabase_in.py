"""Test the Supabase .filter() syntax directly."""
import sys
sys.path.insert(0, '.')
from datetime import datetime
from app.config.database import get_supabase

db = get_supabase()
u = db.table('users').select('*').eq('phone', '9999900003').execute().data[0]
user_id = u['id']
current_month = datetime.now().strftime('%Y-%m')
hw = db.table('household_workers').select('worker_id').eq('household_id', user_id).execute().data[0]
worker_id = hw['worker_id']

print('Testing .filter() IN syntax...')
try:
    r = (
        db.table('payments')
        .select('id')
        .eq('household_id', user_id)
        .eq('worker_id', worker_id)
        .eq('payment_month', current_month)
        .filter('status', 'in', '("processed","pending")')
        .execute()
    )
    print('Result:', r.data)
    print('FILTER OK')
except Exception as e:
    print('FILTER FAILED:', e)

# Fallback approach: two separate queries ORed together
print()
print('Testing two separate eq queries approach...')
try:
    r1 = db.table('payments').select('id').eq('household_id', user_id).eq('worker_id', worker_id).eq('payment_month', current_month).eq('status', 'processed').execute()
    r2 = db.table('payments').select('id').eq('household_id', user_id).eq('worker_id', worker_id).eq('payment_month', current_month).eq('status', 'pending').execute()
    combined = (r1.data or []) + (r2.data or [])
    print('Combined result:', combined)
    print('DOUBLE EQ OK')
except Exception as e:
    print('DOUBLE EQ FAILED:', e)
