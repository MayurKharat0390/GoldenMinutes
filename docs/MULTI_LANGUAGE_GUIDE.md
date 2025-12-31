# 🌐 Multi-Language Support - Implementation Guide

## ✅ **What's Been Configured:**

### 1. Django Settings Updated ✅
- Added `LocaleMiddleware` to MIDDLEWARE
- Configured 3 languages: English, Hindi (हिंदी), Marathi (मराठी)
- Set up LOCALE_PATHS for translation files
- Enabled USE_I18N and USE_L10N

---

## 📋 **Complete Implementation Steps:**

### Step 1: Create Locale Directory Structure
```bash
mkdir locale
mkdir locale\hi
mkdir locale\hi\LC_MESSAGES
mkdir locale\mr
mkdir locale\mr\LC_MESSAGES
```

### Step 2: Add Language Switcher to Base Template

Add this to `templates/base.html` in the navigation:

```html
{% load i18n %}

<!-- Language Switcher -->
<li class="nav-item dropdown">
    <a class="nav-link dropdown-toggle text-dark fw-medium" href="#" data-bs-toggle="dropdown">
        <i class="bi bi-translate me-1"></i>
        {% if LANGUAGE_CODE == 'hi' %}हिंदी{% elif LANGUAGE_CODE == 'mr' %}मराठी{% else %}English{% endif %}
    </a>
    <ul class="dropdown-menu">
        <li>
            <form action="{% url 'set_language' %}" method="post">
                {% csrf_token %}
                <input name="next" type="hidden" value="{{ request.path }}">
                <input name="language" type="hidden" value="en">
                <button type="submit" class="dropdown-item">English</button>
            </form>
        </li>
        <li>
            <form action="{% url 'set_language' %}" method="post">
                {% csrf_token %}
                <input name="next" type="hidden" value="{{ request.path }}">
                <input name="language" type="hidden" value="hi">
                <button type="submit" class="dropdown-item">हिंदी (Hindi)</button>
            </form>
        </li>
        <li>
            <form action="{% url 'set_language' %}" method="post">
                {% csrf_token %}
                <input name="next" type="hidden" value="{{ request.path }}">
                <input name="language" type="hidden" value="mr">
                <button type="submit" class="dropdown-item">मराठी (Marathi)</button>
            </form>
        </li>
    </ul>
</li>
```

### Step 3: Add Language URL Pattern

In `golden_minutes/urls.py`:

```python
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language

urlpatterns = [
    # ... existing patterns ...
    path('i18n/setlang/', set_language, name='set_language'),
]

# Wrap app URLs with i18n_patterns for language prefix
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('emergencies/', include('emergencies.urls')),
    path('responders/', include('responders.urls')),
    # ... other patterns ...
)
```

### Step 4: Mark Strings for Translation

In templates, wrap text with `{% trans %}`:

```html
{% load i18n %}

<h1>{% trans "Welcome to Golden Minutes" %}</h1>
<button>{% trans "Emergency SOS" %}</button>
<p>{% trans "Lives Saved" %}</p>
```

In Python code, use `gettext_lazy`:

```python
from django.utils.translation import gettext_lazy as _

class Emergency(models.Model):
    EMERGENCY_TYPES = [
        ('medical', _('Medical Emergency')),
        ('accident', _('Accident')),
        ('fire', _('Fire')),
    ]
```

### Step 5: Generate Translation Files

```bash
# Create message files for Hindi
python manage.py makemessages -l hi

# Create message files for Marathi
python manage.py makemessages -l mr
```

This creates:
- `locale/hi/LC_MESSAGES/django.po`
- `locale/mr/LC_MESSAGES/django.po`

### Step 6: Add Translations

Edit the `.po` files:

**locale/hi/LC_MESSAGES/django.po:**
```po
msgid "Welcome to Golden Minutes"
msgstr "गोल्डन मिनट्स में आपका स्वागत है"

msgid "Emergency SOS"
msgstr "आपातकालीन SOS"

msgid "Lives Saved"
msgstr "जीवन बचाए गए"

msgid "Medical Emergency"
msgstr "चिकित्सा आपातकाल"

msgid "Accident"
msgstr "दुर्घटना"

msgid "Fire"
msgstr "आग"
```

**locale/mr/LC_MESSAGES/django.po:**
```po
msgid "Welcome to Golden Minutes"
msgstr "गोल्डन मिनिट्समध्ये आपले स्वागत आहे"

msgid "Emergency SOS"
msgstr "आपत्कालीन SOS"

msgid "Lives Saved"
msgstr "जीवन वाचवले"

msgid "Medical Emergency"
msgstr "वैद्यकीय आपत्कालीन"

msgid "Accident"
msgstr "अपघात"

msgid "Fire"
msgstr "आग"
```

### Step 7: Compile Translations

```bash
python manage.py compilemessages
```

This creates `.mo` files that Django uses.

---

## 🎯 **Key Strings to Translate:**

### Homepage:
- "Golden Minutes"
- "Save Lives in Critical Moments"
- "Emergency SOS"
- "Live Map"
- "Dashboard"
- "Login"
- "Register"

### Emergency Types:
- "Medical Emergency"
- "Accident"
- "Fire"
- "Personal Safety"
- "Disaster"

### Dashboard:
- "Welcome"
- "Total Responses"
- "Lives Saved"
- "Avg Response Time"
- "Rating"
- "Level Progress"
- "Achievements"
- "Leaderboard"

### First-Aid (Bystander Mode):
- "First-Aid Guidance"
- "Help is on the way"
- "Mark Complete"
- "Listen"
- "Emergency Contacts"

---

## 📱 **How It Works:**

1. **User selects language** from dropdown
2. **Django sets language cookie** (`django_language`)
3. **All pages reload** in selected language
4. **Language persists** across sessions

---

## 🔧 **Quick Setup Script:**

Create `setup_i18n.py`:

```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'golden_minutes.settings')
django.setup()

# Create locale directories
os.makedirs('locale/hi/LC_MESSAGES', exist_ok=True)
os.makedirs('locale/mr/LC_MESSAGES', exist_ok=True)

print("✓ Locale directories created")
print("\nNext steps:")
print("1. Add {% load i18n %} to templates")
print("2. Wrap text with {% trans 'text' %}")
print("3. Run: python manage.py makemessages -l hi")
print("4. Run: python manage.py makemessages -l mr")
print("5. Edit .po files with translations")
print("6. Run: python manage.py compilemessages")
```

---

## ✅ **Status:**

**Configured:**
- ✅ Django i18n settings
- ✅ Language middleware
- ✅ 3 languages (English, Hindi, Marathi)
- ✅ Locale paths

**To Complete:**
- ⏳ Add language switcher to navigation
- ⏳ Mark strings for translation
- ⏳ Generate .po files
- ⏳ Add Hindi/Marathi translations
- ⏳ Compile messages

---

## 🎯 **Priority Translations:**

### High Priority (User-Facing):
1. Navigation menu
2. Emergency types
3. SOS button
4. Dashboard stats
5. First-aid instructions

### Medium Priority:
6. Form labels
7. Error messages
8. Success messages
9. Help text

### Low Priority:
10. Admin interface
11. Email templates
12. Documentation

---

## 📚 **Sample Translations:**

### Common Phrases:

| English | Hindi (हिंदी) | Marathi (मराठी) |
|---------|--------------|----------------|
| Emergency | आपातकाल | आपत्कालीन |
| Help | मदद | मदत |
| Save | बचाओ | वाचवा |
| Location | स्थान | स्थान |
| Time | समय | वेळ |
| Distance | दूरी | अंतर |
| Accept | स्वीकार करें | स्वीकारा |
| Decline | अस्वीकार करें | नकार द्या |
| Navigate | नेविगेट करें | मार्गदर्शन करा |

---

## 🚀 **Testing:**

1. **Switch to Hindi:**
   - Click language dropdown
   - Select "हिंदी"
   - Page reloads in Hindi

2. **Switch to Marathi:**
   - Click language dropdown
   - Select "मराठी"
   - Page reloads in Marathi

3. **Back to English:**
   - Click language dropdown
   - Select "English"

---

## 📝 **Notes:**

- Language preference stored in cookie
- Works offline (PWA compatible)
- RTL support not needed (Hindi/Marathi are LTR)
- Can add more languages easily
- Translation files are version-controlled

---

**Multi-language foundation is ready!** 🌐

**Next: Add translations to key pages and test language switching.**
