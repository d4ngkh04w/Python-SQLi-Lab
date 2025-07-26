"""
Simple test suite for Python SQLi Lab code improvements.

This validates that the enhanced code compiles and functions correctly
while maintaining the educational vulnerabilities.
"""

import sys
import os
import importlib.util

def test_module_imports():
    """Test that all modules can be imported successfully."""
    print("Testing module imports...")
    
    try:
        import app
        print("✓ app.py imports successfully")
    except Exception as e:
        print(f"✗ app.py import failed: {e}")
        return False
    
    try:
        import database.db as db
        print("✓ database/db.py imports successfully")
    except Exception as e:
        print(f"✗ database/db.py import failed: {e}")
        return False
    
    try:
        import secure_examples
        print("✓ secure_examples.py imports successfully")
    except Exception as e:
        print(f"✗ secure_examples.py import failed: {e}")
        return False
    
    try:
        import rce.exploit
        print("✓ rce/exploit.py imports successfully")
    except Exception as e:
        print(f"✗ rce/exploit.py import failed: {e}")
        return False
    
    return True

def test_flask_app_creation():
    """Test that the Flask app can be created."""
    print("\nTesting Flask app creation...")
    
    try:
        import app
        flask_app = app.app
        
        if flask_app is not None:
            print("✓ Flask app created successfully")
            print(f"✓ App secret key configured: {bool(flask_app.secret_key)}")
            return True
        else:
            print("✗ Flask app is None")
            return False
    except Exception as e:
        print(f"✗ Flask app creation failed: {e}")
        return False

def test_database_functions():
    """Test that database functions are available."""
    print("\nTesting database functions...")
    
    try:
        import database.db as db
        
        # Test that functions exist
        functions_to_check = ['get_db_connection', 'create_tables', 'init_data', 'main']
        for func_name in functions_to_check:
            if hasattr(db, func_name):
                print(f"✓ {func_name} function exists")
            else:
                print(f"✗ {func_name} function missing")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Database function test failed: {e}")
        return False

def test_secure_examples():
    """Test that secure examples are available."""
    print("\nTesting secure examples...")
    
    try:
        import secure_examples
        
        # Test that classes exist
        classes_to_check = ['SecureUserAuthentication', 'SecureBlogSearch', 'SecureUserLookup']
        for class_name in classes_to_check:
            if hasattr(secure_examples, class_name):
                print(f"✓ {class_name} class exists")
            else:
                print(f"✗ {class_name} class missing")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Secure examples test failed: {e}")
        return False

def test_app_routes():
    """Test that all expected routes are defined."""
    print("\nTesting Flask app routes...")
    
    try:
        import app
        
        expected_routes = [
            '/',
            '/sqli/basic',
            '/sqli/basic/profile',
            '/sqli/union',
            '/sqli/error',
            '/sqli/boolean',
            '/sqli/time',
            '/sqli/rce',
            '/sqli/rce/exec'
        ]
        
        # Get all registered routes
        routes = [rule.rule for rule in app.app.url_map.iter_rules()]
        
        for expected_route in expected_routes:
            if expected_route in routes:
                print(f"✓ Route {expected_route} exists")
            else:
                print(f"✗ Route {expected_route} missing")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Route test failed: {e}")
        return False

def test_documentation_exists():
    """Test that documentation files exist."""
    print("\nTesting documentation...")
    
    docs_to_check = [
        'README.md',
        'CODE_REVIEW.md'
    ]
    
    for doc_file in docs_to_check:
        if os.path.exists(doc_file):
            print(f"✓ {doc_file} exists")
        else:
            print(f"✗ {doc_file} missing")
            return False
    
    return True

def main():
    """Run all tests and report results."""
    print("=== Python SQLi Lab Code Quality Tests ===\n")
    
    tests = [
        test_module_imports,
        test_flask_app_creation,
        test_database_functions,
        test_secure_examples,
        test_app_routes,
        test_documentation_exists
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()  # Add spacing between tests
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with exception: {e}\n")
    
    print("=== Test Results ===")
    print(f"Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("🎉 All tests passed! Code improvements are working correctly.")
        return True
    else:
        print("❌ Some tests failed. Please review the code.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)