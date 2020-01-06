from unittest.mock import patch
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTest(TestCase):
    def test_db_available_waiting(self):
        """Test waiting till database is ready""" # Once db is available, app runs
        with patch('django.db.utils.ConnectionHandler.__getitem__') as ch:
            ch.return_value = True
            call_command('waiting_for_database')
            self.assertEqual(ch.call_count, 1)

    @patch('time.sleep', return_value = True)
    def test_db_waiting_continue(self, time_sec):
        """Test waiting for database"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as ch:
            ch.side_effect = [OperationalError] * 5 # First 5 times when we call errors is being raised
            call_command('waiting_for_database')
            self.assertEqual(ch.call_count, 6)
