from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create a manager account for Anmol Automobile."

    def handle(self, *args, **options):
        User = get_user_model()

        email = input("Manager email: ").strip().lower()
        name = input("Manager name: ").strip()
        phone = input("Manager phone: ").strip()
        password = input("Manager password: ")

        if not email:
            raise CommandError("Email is required.")

        if not name:
            raise CommandError("Name is required.")

        if not password:
            raise CommandError("Password is required.")

        if User.objects.filter(email=email).exists():
            raise CommandError(
                "A user with this email already exists."
            )

        user = User.objects.create_user(
            email=email,
            name=name,
            phone=phone,
            password=password,
            role=User.Role.MANAGER,
            is_staff=True,
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Manager '{user.email}' created successfully."
            )
        )