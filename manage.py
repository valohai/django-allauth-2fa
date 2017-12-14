#!/usr/bin/env python
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.settings')

if __name__ == "__main__":
    from django.core import management

    management.execute_from_command_line()
