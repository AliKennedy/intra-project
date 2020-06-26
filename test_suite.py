import unittest

#import test modules
import test_client as client
import test_server as server
import test_db as db

#initialise
loader = unittest.TestLoader()
suite = unittest.TestSuite()

#add tests
suite.addTests(loader.loadTestsFromModule(client))
suite.addTests(loader.loadTestsFromModule(server))
suite.addTests(loader.loadTestsFromModule(db))

#initialise runner
runner = unittest.TextTestRunner()
results = runner.run(suite)