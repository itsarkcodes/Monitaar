from datetime import datetime
import pytz

ist = pytz.timezone('Asia/Kolkata')

def parse_time_string(time_str):
    if not time_str or time_str.lower() == '24hr':
        return None  # Indicates 24-hour operation
    if time_str.lower() == '24hr':
        return None
    try:
        time_obj = datetime.strptime(time_str.strip(), '%I:%M%p')
    except ValueError:
        try:
            time_obj = datetime.strptime(time_str.strip(), '%I%p')
        except ValueError:
            try:
                time_obj = datetime.strptime(time_str.strip(), '%H:%M')
            except ValueError:
                raise ValueError(f"Invalid time format: {time_str}")
    return time_obj.strftime('%H:%M')

def is_within_operational_hours(start_time_str, end_time_str):
    if not start_time_str and not end_time_str:
        return True  # 24-hour operation
    now_ist = datetime.now(ist).time()
    start_time = datetime.strptime(start_time_str, '%H:%M').time() if start_time_str else datetime.strptime('00:00', '%H:%M').time()
    end_time = datetime.strptime(end_time_str, '%H:%M').time() if end_time_str else datetime.strptime('23:59', '%H:%M').time()
    if start_time <= end_time:
        return start_time <= now_ist <= end_time
    else:
        return now_ist >= start_time or now_ist <= end_time
