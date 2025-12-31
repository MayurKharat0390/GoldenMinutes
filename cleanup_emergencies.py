from emergencies.models import Emergency

# List all emergencies
emergencies = Emergency.objects.all()
print(f'Found {emergencies.count()} emergencies:')
for e in emergencies:
    print(f'  - {e.get_emergency_type_display()} at {e.latitude}, {e.longitude} - Status: {e.status}')

# Delete all
emergencies.delete()
print('\nAll emergencies deleted!')
print('Refresh the map - it should now be clear.')
