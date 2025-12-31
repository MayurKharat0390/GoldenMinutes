# 🔒 CONFIDENTIAL: Badge Logic & Triggers

**⚠️ FOR ADMIN EYES ONLY**
Do not share exact thresholds with users to prevent gaming the gamification system.

---

## 🏆 **Badge Trigger Logic**

The system automatically checks these conditions every time an emergency response is completed.

### 📊 **Volume-Based Badges**
*Badges for consistent activity. Hard to fake without actual effort.*

| Badge Name | Trigger Condition | Code Logic |
|------------|------------------|------------|
| **First Responder** | 1 Total Response | `stats.total_responses >= 1` |
| **Dedicated Helper** | 10 Total Responses | `stats.total_responses >= 10` |
| **Community Guardian** | 50 Total Responses | `stats.total_responses >= 50` |
| **Century Club** | 100 Total Responses | `stats.total_responses >= 100` |

### ⚡ **Performance-Based Badges**
*Badges for speed and quality. These are calculated based on timestamps.*

| Badge Name | Trigger Condition | Code Logic |
|------------|------------------|------------|
| **Speed Demon** | Avg Response < 3 mins | `stats.average_response_time <= 3.0` |
| **The Flash** | Avg Response < 1 min | `stats.average_response_time <= 1.0` |
| **Perfect Score** | *DEPRECATED* | *Rating system removed* |

### 📅 **Time/Habit Badges**
*Encourages availability during specific times.*

| Badge Name | Trigger Condition | Code Logic |
|------------|------------------|------------|
| **Streak Master** | 30 Days Consecutive | `stats.current_streak >= 30` |
| **Night Owl** | 10 Responses (10PM-6AM) | *Logic pending implementation* |
| **Early Bird** | 10 Responses (5AM-8AM) | *Logic pending implementation* |

### ❤️ **Impact Badges**
*Highest honor badges. Can only be triggered by confirmed outcomes.*

| Badge Name | Trigger Condition | Code Logic |
|------------|------------------|------------|
| **Life Saver** | 10 Confirmed Saves | `stats.lives_saved >= 10` |
| **Hero of the City** | 50 Confirmed Saves | `stats.lives_saved >= 50` |

---

## 🛡️ **Anti-Gaming Measures**

To prevent users from faking stats:

1. **Unique Emergencies Only**: Multiple responses to the same dummy emergency do NOT count.
2. **Time Validation**: Responses with `response_time < 0` or impossibly fast times (e.g., 1 second for 10km) should be flagged.
3. **Admin Verification**: "Life Saver" counts should require admin or medical staff verification checkbox in the backend.

---

## 🔧 **Admin Tools**

### Check specific user:
```bash
python manage.py award_badges --user username
```

### Reset user stats (if caught cheating):
Admin Panel > Responders > Responder Stats > Reset
