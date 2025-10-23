import unittest
import sys
import os

# Add modules to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))

from id_prefix import set_prefix
from vaults_converter import convert

from id_prefix import set_prefix
from vaults_converter import convert

class TestVaultsConverter(unittest.TestCase):

    def test_convert_vaults(self):
        set_prefix('tenant')
        # Sample input data for vaults
        source_data = {
            'seaf.ta.reverse.cloud_ru.advanced.vaults': {
                'tenant.vaults.25bd50a1-20a3-4ca7-b84a-d9f6dda9a65c': {
                    'id': '25bd50a1-20a3-4ca7-b84a-d9f6dda9a65c',
                    'name': 'Daily_Backups',
                    'description': 'Daily backup vault',
                    'resources': [
                        {
                            'id': 'e5e60a69-0653-4297-8799-ea0df4f0cacc',
                            'type': 'OS::Nova::Server',
                            'name': 'ecs-prod-someserver1',
                            'size': 440, # This is limit size in GB
                            'backup_size': 631900, # This is current backup size in bytes
                            'backup_count': 14,
                            'protect_status': 'available',
                            'extra_info': {}
                        },
                        {
                            'id': 'fb77c40e-b1e2-4aa5-89a9-45725b7ccf30',
                            'type': 'OS::Nova::Server',
                            'name': 'ecs-prod-someserver2',
                            'size': 50,
                            'backup_size': 55736,
                            'backup_count': 14,
                            'protect_status': 'available',
                            'extra_info': {}
                        }
                    ],
                    'tenant': '9f7dcs8823ed23e9cwe223ecwe22236',
                    'DC': 'tenant.dc.01'
                }
            }
        }

        # Expected output
        expected_output = {
            'seaf.ta.services.storage': {
                'tenant.vaults.25bd50a1-20a3-4ca7-b84a-d9f6dda9a65c': {
                    'title': 'Daily_Backups',
                    'description': 'Daily backup vault\nTenant: 9f7dcs8823ed23e9cwe223ecwe22236',
                    'external_id': '25bd50a1-20a3-4ca7-b84a-d9f6dda9a65c',
                    'type': 'Simple Storage Service', # Changed
                    'software': 'Cloud Backup Service',
                    'availabilityzone': [],
                    'location': ['tenant.dc.01'],
                    'network_connection': [],
                    'sla': None,
                }
            },            'seaf.ta.services.backup': {
                'tenant.vaults.25bd50a1-20a3-4ca7-b84a-d9f6dda9a65c.e5e60a69-0653-4297-8799-ea0df4f0cacc': {
                    'title': 'Backup for ecs-prod-someserver1',
                    'description': 'Resource Name: ecs-prod-someserver1\nResource Type: OS::Nova::Server\nLimit Size: 440 GB\nCurrent Size: 0.0 GB\nBackup Count: 14\nProtect Status: available\nExtra Info: {}',
                    'external_id': 'e5e60a69-0653-4297-8799-ea0df4f0cacc',
                    'path': 'Vault: Daily_Backups',
                    'replication': None,
                    'network_connection': [],
                    'availabilityzone': [],
                    'location': ['tenant.dc.01'],
                    'storage': 'tenant.vaults.25bd50a1-20a3-4ca7-b84a-d9f6dda9a65c'
                },
                'tenant.vaults.25bd50a1-20a3-4ca7-b84a-d9f6dda9a65c.fb77c40e-b1e2-4aa5-89a9-45725b7ccf30': {
                    'title': 'Backup for ecs-prod-someserver2',
                    'description': 'Resource Name: ecs-prod-someserver2\nResource Type: OS::Nova::Server\nLimit Size: 50 GB\nCurrent Size: 0.0 GB\nBackup Count: 14\nProtect Status: available\nExtra Info: {}',
                    'external_id': 'fb77c40e-b1e2-4aa5-89a9-45725b7ccf30',
                    'path': 'Vault: Daily_Backups',
                    'replication': None,
                    'network_connection': [],
                    'availabilityzone': [],
                    'location': ['tenant.dc.01'],
                    'storage': 'tenant.vaults.25bd50a1-20a3-4ca7-b84a-d9f6dda9a65c'
                }
            }
        }

        # Run the conversion
        converted_data = convert(source_data)

        # Assert that the result is as expected
        self.assertEqual(converted_data, expected_output)

if __name__ == '__main__':
    unittest.main()
