# Quick Fix for Template Error

## Issue:
Line 90-91 in `templates/base.html` has a broken template tag.

## Current (BROKEN):
```html
{% if LANGUAGE_CODE == 'hi' %}हिंदी{% elif LANGUAGE_CODE == 'mr' %}मराठी{% else %}English{%
endif %}
```

## Should Be (FIXED):
```html
{% if LANGUAGE_CODE == 'hi' %}हिंदी{% elif LANGUAGE_CODE == 'mr' %}मराठी{% else %}English{% endif %}
```

## Manual Fix Steps:

1. Open `d:\Golden Minutes\templates\base.html`
2. Go to line 90
3. Find this text:
   ```
   {% if LANGUAGE_CODE == 'hi' %}हिंदी{% elif LANGUAGE_CODE == 'mr' %}मराठी{% else %}English{%
   endif %}
   ```
4. Replace with (all on ONE line):
   ```
   {% if LANGUAGE_CODE == 'hi' %}हिंदी{% elif LANGUAGE_CODE == 'mr' %}मराठी{% else %}English{% endif %}
   ```
5. Save the file
6. Refresh browser

The problem is the `{% endif %}` is on a separate line from the rest of the if statement.
