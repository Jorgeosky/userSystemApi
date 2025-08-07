from django.db import migrations

def create_superadmin(apps, schema_editor):
    CustomUser = apps.get_model('users', 'CustomUser')  # Cambia aquí el nombre del modelo
    if not CustomUser.objects.filter(username='admin').exists():
        CustomUser.objects.create_superuser(
            username='admin',
            email='admin@localhost',
            password='admin'
        )

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('users', '0002_customuser_voucher'),
    ]

    operations = [
        migrations.RunPython(create_superadmin),
    ]
