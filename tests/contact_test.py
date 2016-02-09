import unittest
import sys
sys.path.append('..')
import database

# Basic tests for CRUD
class ContactTest(unittest.TestCase):

    def setUp(self):
        self.user_id = 1

    def test_single_contact_life_cycle(self):
        contact_info = {
        'first_name':'test_first_name',
        'last_name':'test_last_name',
        'email':'test_email',
        'phone_number':'0123456789'
        }
        # Create the contact and assert it's existence and confirm the database created it
        contact_insertion = database.insert_contact(contact_info, self.user_id)
        self.assertTrue(contact_insertion['created'])
        self.assertIsNotNone(contact_insertion['contact_id'])
        contact_id = contact_insertion['contact_id']

        # Read the contact just created
        contact = database.get_contact_with_id(contact_id)
        self.assertIsNotNone(contact)

        # Edit the contact just read
        update_info = {
        'first_name':'update_first_name',
        'last_name':'update_last_name',
        'email':'update_email',
        'phone_number':'0123456789876543210',
        'contact_id':contact_id
        }
        contact_update = database.update_contact(update_info)
        self.assertTrue(contact_update['updated'])

        # Delete the contact just updated
        contact_deletion = database.delete_contact(contact_id)
        self.assertTrue(contact_deletion['deleted'])
        # To confirm, try to get the contact with the same id and make sure we get None back
        contact = database.get_contact_with_id(contact_id)
        self.assertIsNone(contact)

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()